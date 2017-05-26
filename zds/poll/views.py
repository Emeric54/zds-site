#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from zds.poll.forms import PollForm
from zds.poll.models import Poll
from zds.tutorialv2.models.models_database import PublishableContent
from zds.utils import slugify


class NewPoll(CreateView):
    model = Poll
    template_name = 'poll/new.html'
    form_class = PollForm

    def get_context_data(self, **kwargs):
        context = super(NewPoll, self).get_context_data(**kwargs)
        content_id = self.request.GET['contenu']
        context['content'] = get_object_or_404(PublishableContent, id=content_id)
        content = PublishableContent.objects.get(id=content_id)

        if content.type != 'OPINION':
            raise PermissionDenied

        if self.request.user not in content.authors.all():
            raise PermissionDenied

        return context

    def form_valid(self, form):
        poll = form.save(commit=False)
        poll.slug = slugify(form.cleaned_data['title'])
        return self.render_to_response(self.get_context_data(form=form))
