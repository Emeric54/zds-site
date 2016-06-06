#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from zds.poll.api.serializers import PollDetailSerializer, UsersSerializers
from zds.poll.models import Poll, Choice


class PollDetailAPIView(RetrieveAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    renderer_classes = (JSONRenderer,)


class UsersDetailAPIView(RetrieveAPIView):

    queryset = Choice.objects.all()
    serializer_class = UsersSerializers
