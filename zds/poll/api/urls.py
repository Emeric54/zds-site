# coding: utf-8

from django.conf.urls import url

from zds.poll.api.views import PollDetailAPIView, UsersDetailAPIView, VoteAPIView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', PollDetailAPIView.as_view(), name='detail'),
    url(r'^choix/(?P<pk>[0-9]+)/$', UsersDetailAPIView.as_view(), name='detail'),
    url(r'^vote/(?P<pk>[0-9]+)/$', VoteAPIView.as_view(), name='vote'),
]
