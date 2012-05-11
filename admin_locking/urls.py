from django.conf.urls.defaults import patterns

urlpatterns = patterns('admin_locking.views',
    (r'^unlock/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)$', 'unlock'),
)
