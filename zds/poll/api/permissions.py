#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import permissions


class AccessUsersPermission(permissions.BasePermission):
    """
    if the vote is anonymous : false
    if the vote isn't anonymous : true
    """

    def has_object_permission(self, request, view, obj):
        if obj.poll.anonymous_vote:
            return False
        else:
            return True
