#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from zds.poll.api.serializers import PollListSerializer, PollDetailSerializer
from zds.poll.models import Poll


class PollListAPIView(ListAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetailAPIView(RetrieveAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    renderer_classes = (JSONRenderer,)

