from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.modules_index, name="modules_table"),
    url(r'^(?P<module_id>[0-9]+)/$', views.modules_students, name = "students_enrolled"),
    url(r'^list$', views.students_list, name="modules_table"),
]
