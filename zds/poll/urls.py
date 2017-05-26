#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from zds.poll.views import NewPoll

urlpatterns = [
    url(r'^nouveau/$', NewPoll.as_view(), name='poll-new'),
]
