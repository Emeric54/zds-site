# coding: utf-8

import datetime

from django.test import TestCase

from zds.poll.forms import PollForm, UpdatePollForm
from zds.poll.models import UNIQUE_VOTE_KEY, MULTIPLE_VOTE_KEY


class PollFormTest(TestCase):

    def test_valid_poll_form(self):
        data = {
            'title': 'Test poll',
            'anonymous_vote': True,
            'enddate': datetime.datetime.today() + datetime.timedelta(1),
            'type_vote': UNIQUE_VOTE_KEY
        }
        form = PollForm(data=data)

        self.assertTrue(form.is_valid())

    def test_invalid_poll_form_empty_title(self):
        data = {
            'title': '',
            'anonymous_vote': False,
            'enddate': datetime.datetime.today() + datetime.timedelta(5),
            'type_vote': MULTIPLE_VOTE_KEY
        }
        form = PollForm(data=data)

        self.assertFalse(form.is_valid())

    def test_invalid_poll_form_no_title(self):
        data = {
            'anonymous_vote': False,
            'type_vote': MULTIPLE_VOTE_KEY
        }
        form = PollForm(data=data)

        self.assertFalse(form.is_valid())

    def test_invalid_poll_form_bad_enddate(self):
        data = {
            'title': 'Test poll',
            'anonymous_vote': False,
            'enddate': datetime.datetime.today(),
            'type_vote': MULTIPLE_VOTE_KEY
        }
        form = PollForm(data=data)

        self.assertFalse(form.is_valid())


class UpdatePollFormTests(TestCase):

    def test_valid_update_poll_form_new_enddate(self):
        data = {
            'enddate': datetime.datetime.today() + datetime.timedelta(1)
        }
        form = UpdatePollForm(data=data)

        self.assertTrue(form.is_valid())

    def test_valid_update_poll_form_desactivate(self):
        data = {
            'activate': False
        }
        form = UpdatePollForm(data=data)

        self.assertTrue(form.is_valid())
