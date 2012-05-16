import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Lock(models.Model):
    user = models.ForeignKey("auth.User")
    until = models.FloatField(_('Locked until'))
    content_type_id = models.IntegerField(_('Content type id'))
    object_id = models.IntegerField(_('Object id'))
    
    class Meta:
        verbose_name = _('Lock')
        verbose_name_plural = _('Locks')
        
class ObjectChangelog(models.Model):
    user = models.ForeignKey("auth.User")
    time = models.FloatField(_('Time'))
    content_type_id = models.IntegerField(_('Content type id'))
    object_id = models.IntegerField(_('Object id'))
    
    class Meta:
        verbose_name = _('Object changelog entry')
        verbose_name_plural = _('Object changelog entries')
