# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db import models


class Request(models.Model):

	class Meta:
		verbose_name = 'Request'
		verbose_name_plural = 'Requests'
		ordering = ['-pubdate']
	
	title = models.CharField('Titre de la demande', max_length=80)
	slug = models.SlugField(max_length=80)
	subtitle = models.CharField('Sous-titre de la demande', max_length=120, blank=True)
	comment = models.TextField('Commentaire du demandeur')
	user = models.ForeignKey(User, verbose_name =(u'Membre'), db_index=True)
	pubdate = models.DateTimeField(u'Date de création', auto_now_add=True, db_index=True)


	def __unicode__(self):
		"""Human-readable representation of the Request model.
        
        :return: Request title
        :rtype: unicode
        """
		return self.title

	def get_absolute_url(self):
		"""URL of a single Request.
        
        :return: Requestobject URL
        :rtype: str
        """
		return reverse('request-details', args=[self.pk])