#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from zds.tutorialv2.models.models_database import PublishableContent


class Poll(models.Model):

    class Meta:
        verbose_name = 'Sondage'
        verbose_name_plural = 'Sondages'

    title = models.CharField('Titre', max_length=80)
    slug = models.SlugField(max_length=80)
    content = models.ForeignKey(PublishableContent, verbose_name='Auteur')

    anonymous_vote = models.BooleanField('Vote anonyme', default=True)
    multiple_vote = models.BooleanField('Vote multiple', default=False)

    def __unicode__(self):
        """
        Human-readable representation of the Poll model.
        :return: Poll title
        :rtype: unicode
        """
        return self.title

    def get_count_users(self):
        """
        :return: The number of user who has voted.
        :rtype: int
        """
        count = self.get_vote_classe().objects.filter(poll=self).values('poll').annotate(Count('user', distinct=True))
        if count:
            return count[0]['user_count']
        else:
            return 0

    def get_vote_class(self):
        if self.multiple_vote:
            return MultipleVote
        elif not self.multiple_vote:
            return UniqueVote
        raise TypeError


class Choice(models.Model):

    class Meta:
        verbose_name = 'Choix'
        verbose_name_plural = 'Choix'

    choice = models.CharField('Choix', max_length=200)
    poll = models.ForeignKey(Poll, related_name='choices', null=False, blank=False, verbose_name='sondage')

    def __unicode__(self):
        """
        Human-readable representation of the Choice model.
        :return: Choice
        :rtype: unicode
        """
        return self.choice

    def get_count_votes(self):
        """
        :return: The count of votes for this choice
        :rtype: int
        """
        count = self.poll.get_vote_class().objects.filter(choice=self, poll=self.poll).count()
        return count

    def get_users(self):
        """
        :return: Users
        :rtype: a list
        """
        return [Vote.user for Vote in self.poll.get_vote_class().objects.filter(choice=self, poll=self.poll)]

    def set_user_vote(self, user):
        if self.poll.multiple_vote:
            UniqueVote.objects.update_or_create(user=user, choice=self, poll=self.poll)
        elif not self.poll.multiple_vote:
            MultipleVote.objects.update_or_create(user=user, choice=self, poll=self.poll)


class Vote(models.Model):

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ('user', 'choice')
        abstract = True

    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice, blank=False)
    user = models.ForeignKey(User)


class UniqueVote(Vote):
    """
    Unique vote allow a member to vote for only one choice.
    """

    class Meta:
        verbose_name = 'Vote unique'
        verbose_name_plural = 'Votes uniques'
        unique_together = (('user', 'choice'), ('user', 'poll'))


class MultipleVote(Vote):
    """
    Multiple Vote allow member to vote for one or more choices.
    """

    class Meta:
        verbose_name = 'Vote multiple'
        verbose_name_plural = 'Votes multiples'
        unique_together = ('user', 'choice', 'poll')
