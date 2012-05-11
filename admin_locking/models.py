import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Lock(models.Model):
    user = models.ForeignKey("auth.User")
    until = models.FloatField(_('Locked until'))
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    
class ObjectChangelog(models.Model):
    user = models.ForeignKey("auth.User")
    time = models.FloatField()
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()