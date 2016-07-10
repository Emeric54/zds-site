#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer

from zds.poll.api.serializers import PollDetailSerializer, UsersSerializers, VoteSerializer
from zds.poll.models import Poll, Choice
from zds.poll.api.permissions import AccessUsersPermission


class PollDetailAPIView(RetrieveAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    renderer_classes = (JSONRenderer,)


class UsersDetailAPIView(RetrieveAPIView):

    permission_classes = (AccessUsersPermission,)
    queryset = Choice.objects.all()
    serializer_class = UsersSerializers
    renderer_classes = (JSONRenderer,)


class VoteAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Choice.objects.all()
    serializer_class = VoteSerializer
    renderer_classes = (JSONRenderer,)

