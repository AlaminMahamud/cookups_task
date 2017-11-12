#-*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^polls/$', views.poll_list),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.poll_detail),

    # filtering would work if i tweak a little
    url(r'^polls/(?P<pk>[0-9]+)/', views.PollList.as_view())
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
#    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
]
