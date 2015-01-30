from django.conf.urls import patterns, url

from syslogs.views import system_log, new_logs

urlpatterns = patterns(
    '',
    url(r'^$', system_log),
    url(r'^new_logs/$', new_logs),
)
