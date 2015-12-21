from django.conf.urls import url

from zds.contentrequest.views import ListRequest, NewRequest, DetailsRequest

urlpatterns = [
    url(r'^$', ListRequest.as_view(), name='request-list'),
    url(r'^nouveau/$', NewRequest.as_view(), name='request-new'),
    url(r'^(?P<pk>\d+)/$', DetailsRequest.as_view(), name='request-details'),
]