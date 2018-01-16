# views that don't need their own file

from django.contrib import messages
from social.models import Post, Notification
from social.notifications import Notify
from social.collections import Collections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

data = {}
c = Collections()
pages_dir = 'social/pages/'

def index(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/home')

  popular_posts = c.popular(request.user)[:3]
  return render(request, pages_dir + 'landing/index.html', {'popular_posts': popular_posts})


@login_required
def home(request):
  # get posts
  data['posts'] = c.feed(request.user)[:15]
  data['posts_count'] = len(c.feed(request.user))

  data['page'] = 'home'
  return render(request, pages_dir + 'home.html', data)


def explore_posts(request):
  data['posts'] = c.popular(request.user)[:15]
  data['posts_count'] = len(c.popular(request.user))

  return render(request, pages_dir + 'explore-posts.html', data)


@login_required
def explore_users(request):
  data['users'] = c.popular_users(request.user)[:15]
  data['users_count'] = len(c.popular_users(request.user))

  return render(request, pages_dir + 'explore-people.html', data)


def posts(request, url):
  # get post
  try:
    post = Post.objects.get(url='/p/'+url+'/')
  except Post.DoesNotExist:
    raise Http404("Post does not exist!")

  # get related posts
  # related_posts = c.related_posts(post)
  # post comments
  comments = post.get_comments()

  data = {
    'post': post, 
    'comments': comments[:10], 
    # 'related_posts': related_posts
  }

  # has this post been liked by the current user?
  if request.user.is_authenticated():
    is_liked = post.get_likes().filter(item_id=post.id, item_type="post", user=request.user).exists()
    data['is_liked'] = is_liked

  return render(request, pages_dir + 'post.html', data)


@login_required
def notifications(request):
  notifs = Notification.objects.filter(target_type="user", target_id=request.user.id).order_by('-created_at')
  notifications = []
  for n in notifs[:10]:
    notif = Notify(n)
    notification = notif.get()
    notifications.append({'message': notification, 'created_at': n.created_at})
    # mark unread notification as read
    if n.is_read == False:
      n.is_read = True
      n.save()

  data['notifications'] = notifications
  data['notifs_count'] = notifs.count()
  data['page'] = 'notifs'
  return render(request, pages_dir + 'user-notifications.html', data)