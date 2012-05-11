"""
These functions represents the stable api for admin_locking. All other code
is subject to change.
"""

import time

from django.contrib.contenttypes.models import ContentType

from admin_locking import assert_no_lock_exists, unlock_raw
from admin_locking.models import Lock, ObjectChangelog
from admin_locking.settings import ADMIN_LOCKING

def lock(obj, user, steal=False):
    """
    Locks the object for the user. If it is already locked and "steal" is not
    activated, a "LockExistsException" is thrown.
    """
    if not steal:
        assert_no_lock_exists(obj, user)
    unlock(obj)
    content_type_id = ContentType.objects.get_for_model(obj).pk
    Lock(
        by = user,
        until = time.time() + ADMIN_LOCKING['lock_duration'],
        content_type_id = content_type_id,
        object_id = obj.pk,
    ).save()

def unlock(obj):
    """
    Unlocks the object.
    """
    content_type_id = ContentType.objects.get_for_model(obj).pk
    unlock_raw(content_type_id, obj.pk)


def log_change(obj, user):
    """
    Logs a change of the object given.
    """
    content_type_id = ContentType.objects.get_for_model(obj).pk
    ObjectChangelog(by=user, time=time.time(),
        content_type_id=content_type_id, object_id = obj.pk).save()