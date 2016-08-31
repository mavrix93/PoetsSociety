from django.conf.urls import url
from . import views
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.poem_list, name='poem_list'),
    url(r'^poems/(?P<pk>\d+)/$', views.poem_detail, name='poem_detail'),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^new_poem/$', views.poem_new, name='poem_new'),
    url(r'^poems/(?P<pk>\d+)/edit/$', views.poem_edit, name='poem_edit'),
    url(r'^poems/(?P<pk>\d+)/remove/$', views.poem_remove, name='poem_remove'),
    url(r'^society/(?P<group_name>[a-zA-Z\s]*)$', views.group_poem_list, name='group_poem_list'),
    url(r'^drafts/$', views.draft_poem_list, name='draft_poem_list'),
    url(r'^groups/$', views.groups_list, name='groups_list'),
    url(r'^my_poems/$', views.my_poem_list, name='my_poem_list'),
]