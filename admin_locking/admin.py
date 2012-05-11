import time
import copy
import datetime

from django.contrib import admin
from django import forms
from django.forms.widgets import HiddenInput
from django.contrib import messages
from django.contrib.admin.util import unquote
from django.template.loader import render_to_string

from admin_locking.exceptions import ObjectChangedException, LockExistsException
from admin_locking import (assert_no_lock_exists, 
                           assert_object_not_changed_since)
from admin_locking.api import lock, unlock

LOCK_ERROR_TEMPLATE_NAME = "admin_locking/lock_error.html"
PAGE_LOAD_TIME_ERROR_TEMPLATE_NAME = "admin_locking/page_load_time_error.html"

def render_error(template_name, request, obj):
    return render_to_string(template_name, dict(
        obj = obj,
        until = (datetime.datetime.fromtimestamp(obj.until) 
                 if hasattr(obj, 'until') else None),
        time = (datetime.datetime.fromtimestamp(obj.time) 
                 if hasattr(obj, 'time') else None),
        request = request,
    ))
    
def try_lock(obj, request, show_message=False):
    try:
        lock(obj, request.user)
    except LockExistsException as e:
        if not show_message:
            raise forms.ValidationError(render_error(LOCK_ERROR_TEMPLATE_NAME, 
                                               request, e.obj))
        else:
            if request.method == 'GET':
                messages.add_message(request, messages.ERROR, 
                    render_error(LOCK_ERROR_TEMPLATE_NAME, request, e.obj))
                                
class LockingAdmin(admin.ModelAdmin):
    class Media():
        js = ('admin_locking/js/admin_locking.js', )
        
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(LockingAdmin, self).get_form(request, obj=None, **kwargs)
        
        if obj is None:
            return form
         
        def try_load_time(on_exception_do):
            try:
                load_time = request.POST['admin_locking_page_load_time']
                assert_object_not_changed_since(obj, load_time)
            except ObjectChangedException as e:
                on_exception_do(e.obj)
                
        class ExtendedForm(form):
            admin_locking_page_load_time = forms.FloatField(
                initial=time.time(), widget=HiddenInput())
            
            def clean(self, *args, **kwargs):
                def page_load_time_error(obj):
                    raise forms.ValidationError(render_error(
                        PAGE_LOAD_TIME_ERROR_TEMPLATE_NAME, request, obj))
                try_lock(obj, request)
                try_load_time(page_load_time_error)
                return super(ExtendedForm, self).clean(*args, **kwargs)
        
        return ExtendedForm
    
    def get_fieldsets(self, request, obj=None, *args, **kwargs):
        fieldsets = super(LockingAdmin, self).get_fieldsets(request, obj=obj, 
                                                            *args, **kwargs)
        if obj is not None:
            fieldsets = copy.deepcopy(fieldsets)
            fields = fieldsets[0][1]['fields']
            if 'admin_locking_page_load_time' not in fields:
                fields.extend(['admin_locking_page_load_time'])
        
        return fieldsets 
    
    def save_model(self, request, obj, form, change):
        def assertions(obj, request):
            assert_no_lock_exists(obj, request.user)
            load_time = request.POST['admin_locking_page_load_time']
            assert_object_not_changed_since(obj, load_time)
                
        if obj is not None:
            assertions(obj, request)
            add_object_changelog(obj, request)
            
        return super(LockingAdmin, self).save_model(request, obj, form, change)
    
    def change_view(self, request, object_id, *args, **kwargs):
        obj = self.get_object(request, unquote(object_id))
        try_lock(obj, request, True)
        return super(LockingAdmin, self).change_view(request, object_id, 
                                                     *args, **kwargs)
        
    def response_change(self, request, obj, *args, **kwargs):
        response = super(LockingAdmin, self).response_change(request, obj, 
                                                             *args, **kwargs)
        continuations = ("_continue", "_saveasnew", "_addanother")
        if any(x in request.POST for x in continuations):
            return response
        
        if obj is not None:
            unlock(obj)
            
        return response
        