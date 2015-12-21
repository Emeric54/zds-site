#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from zds.contentrequest.models import Request

class RequestForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ['title', 'subtitle', 'comment']

	def __init__(self, *args, **kwargs):
		super(RequestForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False

		self.helper.layout = Layout(
			Field('title'),
			Field('subtitle'),
			Field('comment')
		)

	def clean(self):
		cleaned_data = super(RequestForm, self).clean()

		title = cleaned_data.get('title')

		if title and title.strip() == '':
			self._errors['title'] = self.error_class(
				['Vous devez donner un titre à votre demande'])
			if 'title' in cleaned_data:
				del cleaned_data['title']

		comment = cleaned_data.get('comment')

		if comment and comment.strip() == '':
			self._errors['comment'] = self.error_class(
				['Vous devez inclure un commentaire à votre demande'])
			if 'comment' in cleaned_data:
				del cleaned_data['comment']

		return cleaned_data