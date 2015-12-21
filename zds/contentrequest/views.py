from django.views.generic import TemplateView, FormView
from django.views.generic import DetailView
from django.shortcuts import redirect

from zds.contentrequest.forms import RequestForm
from zds.contentrequest.models import Request
from zds.member.decorator import LoginRequiredMixin
from zds.utils.paginator import ZdSPagingListView
from zds.utils import slugify


class ListRequest(ZdSPagingListView):
	
	model = Request
	template_name = 'contentrequest/list.html'
	context_object_name = 'requests'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(ListRequest, self).get_context_data(**kwargs)

		context['requests'] = Request.objects.all()

		return context


class NewRequest(LoginRequiredMixin, FormView):

	template_name = 'contentrequest/new.html'
	form_class = RequestForm

	def get_context_data(self, **kwargs):
		context = super(NewRequest, self).get_context_data(**kwargs)
		
		return context

	def form_valid(self, form):
		request = form.save(commit=False)
		request.user = self.request.user
		request.slug = slugify(form.cleaned_data['title'])

		formset = RequestForm(self.request.POST, instance=request)
		if formset.is_valid():
			request.save()
			formset.save()
		else:
			return self.render_to_response(self.get_context_data(form=form))
		return redirect('request-list')


class DetailsRequest(DetailView):
	model = Request
	template_name = 'contentrequest/detail.html'
	context_object_name = 'request'

	def get_context_data(self, **kwargs):
		context = super(DetailsRequest, self).get_context_data(**kwargs)
		request = context['request']

		return context