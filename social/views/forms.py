# views for forms i.e create, edit, search forms etc

from django.contrib import messages
from social.models import Post, Notification
from social.forms import PostForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from watson import search as watson
from django.contrib.auth.decorators import login_required

pages_dir = 'social/pages/'

@login_required
def post(request):
	data = {}
	if request.method == 'POST':
		url = request.POST.get('url', None)
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			# create or update
			post = Post() if url is None else Post.objects.get(url=url)
			post.title = request.POST['title']
			post.content = request.POST['content']
			post.author = request.user
			# add image if uploaded
			featured_image = request.FILES.get('featured_image', False)
			if featured_image:
				post.featured_image = featured_image
			post.save()

			data['errors'] = False
			data['next'] = post.url # redirect url
		else:
			data['errors'] = form.errors
		return JsonResponse(data)

	# GET request
	return HttpResponseRedirect("/home")


def search(request, tag=None):
	data = {}
	template = pages_dir + 'search.html'
	q = request.GET.get('q', '') if tag == None else tag
	if q != '':
		results = watson.search(q)
		data['q'] = q
		data['results_count'] = results.count()
		data['results'] = results[:10]
		data['is_search'] = True if tag == None else False
	return render(request, template, data)