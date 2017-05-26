#!/usr/bin/python
# -*- coding: utf-8 -*-

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from django import forms

from zds.poll.models import Poll


class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ['title', 'anonymous_vote', 'multiple_vote']

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('title'),
            Field('anonymous_vote'),
            Field('multiple_vote'),
        )

        def clean(self):
            cleaned_data = super(PollForm, self).clean()

            title = cleaned_data.get('title')
            if title and title.strip == '':
                self._errors['title'] = self.error_class(
                    [('Le champ titre ne peut être vide.')])
                if 'title' in cleaned_data:
                    del cleaned_data['title']

            return cleaned_data

