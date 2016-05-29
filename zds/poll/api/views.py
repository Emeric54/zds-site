#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from zds.poll.api.serializers import PollDetailSerializer
from zds.poll.models import Poll


class PollDetailAPIView(RetrieveAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    renderer_classes = (JSONRenderer,)

