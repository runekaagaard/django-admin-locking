About
=====

Out of the box the Django administration does not protect its users from the
hazards of concurrent editing. django-admin-locking does the following:

- Locks the content in the admin.
- Prevents saving of stale data. This can happen if user A opens a page, user
  B opens a page, saves and navigates away from the page and user A now saves 
  the page.
- Is helpful towards the users.
- Has a super simple API for use in other apps.

Installation
============

- Add 'admin_locking' to "INSTALLED_APPS" in "settings.py".
- Add the following to "urls.py"::
  
      (r'^admin_locking/', include('admin_locking.urls')),

- Make all your modeladmins extend "LockingAdmin()"::
  
      from admin_locking.admin import LockingAdmin
      class MyModelAdmin(LockingAdmin):
      	  pass