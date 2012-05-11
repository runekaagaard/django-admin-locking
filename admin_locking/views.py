from django.http import HttpResponse
from admin_locking import unlock_raw

def unlock(request, content_type_id, object_id):
    unlock_raw(content_type_id, object_id, request.user)
    return HttpResponse("OK")