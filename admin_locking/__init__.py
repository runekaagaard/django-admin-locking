import time
import datetime

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from admin_locking.models import Lock, ObjectChangelog
from admin_locking.exceptions import (LockExistsException, 
                                      ObjectChangedException)
from admin_locking.settings import ADMIN_LOCKING
    
def raise_if_exists(query, exception=LockExistsException):
    result = query.all()
    if result.exists():
        raise exception(result[0])

def assert_no_lock_exists(obj, user):
    content_type_id = ContentType.objects.get_for_model(obj).pk
    query = Lock.objects.exclude(by=user).filter(
        until__gte=time.time(), content_type_id=content_type_id, 
        object_id=obj.pk).order_by('-pk')
    raise_if_exists(query)
    
def assert_object_not_changed_since(obj, load_time):
        content_type_id = ContentType.objects.get_for_model(obj).pk
        query = ObjectChangelog.objects.filter(time__gte=load_time, 
            content_type_id=content_type_id, object_id=obj.pk).order_by('-pk')
        raise_if_exists(query, ObjectChangedException)
            
def unlock_raw(content_type_id=None, object_id=None, user=None):
    # TODO: Find the correct name.
    locks = Lock.objects
    if content_type_id:
        locks = locks.filter(content_type_id=content_type_id)
    if object_id:
        locks = locks.filter(object_id=object_id)
    if user:
        locks = locks.filter(user=user)
    locks.delete()
        
# Delete all locks when the user logs out.
from django.contrib.auth.signals import user_logged_out
user_logged_out.connect(lambda user, **kwargs: unlock_raw(user=user))
