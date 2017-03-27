from django.conf.urls import url, include
from django.contrib import admin

from app import views as app_views

urlpatterns = [
    url(r'^$', app_views.home),

    url(r'^admin/', admin.site.urls),
    url(r'^email-sent/', app_views.validation_sent),
    url(r'^login/$', app_views.home),
    url(r'^logout/$', app_views.logout),
    url(r'^done/$', app_views.done, name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', app_views.ajax_auth,
        name='ajax-auth'),
    url(r'^email/$', app_views.require_email, name='require_email'),
    # url(r'^modules/new/$', app_views.new_module),

    url(r'^students/$', app_views.students_index, name="students_index"),
    url(r'^students/(?P<id>[0-9]+)/$', app_views.students_show, name="students_show"),

    url(r'^modules/$', app_views.modules_index, name="modules_index"),
    url(r'^modules/(?P<id>[0-9]+)/$', app_views.modules_show, name="modules_show"),

    url(r'^timeslots/(?P<id>[0-9]+)/$', app_views.timeslots_show, name="timeslots_show"),

    url(r'^timeslots/(?P<id>[0-9]+)/upload$', app_views.timeslots_sheet_upload, name="timeslots_sheet_upload"),

    url(r'^timeslots/(?P<id>[0-9]+)/sheet/(?P<page_number>[0-9]+)$', app_views.sheet, name="timeslots_sheet_show"),
    url(r'^timeslots/(?P<id>[0-9]+)/sheet/$', app_views.sheet),

    url(r'', include('social_django.urls'))
]
