from django.conf import settings

ADMIN_LOCKING = {
	# The number of seconds until a lock is lifted.
	'lock_duration': 60 * 60,
}

try:
	ADMIN_LOCKING.update(settings.ADMIN_LOCKING)
except AttributeError:
	pass