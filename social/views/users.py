# views concerned with the User object

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.core.mail import send_mail
from social.collections import Collections
from django.contrib.auth.decorators import login_required

pages_dir = 'social/pages/'
data = {}
c = Collections()

def users(request, username, page=None):
  # get user
  username = username.strip('@') # remove @ char
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    raise Http404("User does not exist!")
  data['krak_user'] = user

  posts = user.profile.get_posts()
  following = list(reversed(user.profile.following.all()))
  followers = list(reversed(user.profile.followers.all()))

  if page is None:
    data['posts'] = posts[:3]
    data['posts_count'] = posts.count()
    data['following_count'] = len(following)
    data['followers_count'] = len(followers)
    # has this user been followed by the current user?
    if request.user.is_authenticated():
      is_followed = user.profile.followers.filter(id=request.user.id).exists()
      data['is_followed'] = is_followed

    template = pages_dir + 'user.html'
  elif page == "posts":
    data['posts'] = posts[:10]
    data['posts_count'] = posts.count()

    template = pages_dir + 'user-posts.html'
  elif page == "following":
    data['users'] = following[:10]
    data['following_count'] = len(following)

    template = pages_dir + 'user-following.html'
  elif page == "followers":
    data['users'] = followers[:10]
    data['followers_count'] = len(followers)

    template = pages_dir + 'user-followers.html'
  elif page == "liked":
    if user == request.user:
      liked_posts = c.liked(request.user)
      data['posts'] = liked_posts[:10]
      data['posts_count'] = liked_posts.count()
      template = pages_dir + 'user-liked.html'
    else:
      return HttpResponseRedirect(user.profile.url)

  return render(request, template, data)

@login_required
def edit_profile(request):
  # For some reason when a requests hits this view
  # data variable (dict) still contains data from users
  # view i.e user, posts etc which is not serialized
  # and returns a 500 on returning a json response.
  # Let's set data to nothing for now while we try to
  # figure the hell what is going on.
  data = {}
  if request.method == 'POST':
    form = EditProfileForm(request.POST)
    if form.is_valid():
      # update user
      user = request.user
      user.profile.full_name = request.POST['full_name']
      user.profile.bio = request.POST['bio']
      user.profile.link = request.POST['link']
      profile_photo = request.FILES.get('profile_photo', False)
      if profile_photo:
        user.profile.profile_photo = profile_photo
      user.profile.save()
      messages.success(request, 'Your profile was edited successfully!')
      data['errors'] = False
    else:
      data['errors'] = form.errors
    return JsonResponse(data)

@login_required
def user_settings(request):
  template = pages_dir + 'settings.html'

  user = request.user
  if not user.is_authenticated():
    messages.info(request, "You're not logged in!")
    return HttpResponseRedirect('/action=sign_in&next='+request.path)

  if request.method == 'POST':
    action = request.POST.get('submit')
    if action == 'change_password':
      change_password_form = PasswordChangeForm(request.user, request.POST)
      if change_password_form.is_valid():
        user = change_password_form.save()
        update_session_auth_hash(request, user) # new session
        messages.success(request, 'Your password was changed successfully!')
        return HttpResponseRedirect(request.user.profile.url)
      else:
        # errors in form...
        messages.error(request, 'Password change failed!')
        data.update({'change_password_form': change_password_form, 'pif': 'settings'})
        return render(request, template, data)

  # serve form
  change_password_form = PasswordChangeForm(request.user)
  data['change_password_form'] = change_password_form

  data['page'] = 'options'
  return render(request, template, data)


def verify(request):
  uid = request.GET.get('uid')

  if User.objects.filter(id=uid).exists():
    user = User.objects.get(id=uid)
    user.profile.is_verified = True
    user.save()
    data['verified'] = True
  else:
    data['verified'] = False
  return render(request, pages_dir + 'verify-account.html', data)


def resend_verification(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      if user.profile.is_verified == False:
        # resend verification email
        subject = 'Verify Your Krak.lol Account'
        message = ''
        from_email = 'noreply@krak.lol'
        recipient_list = (email,)
        html_message = loader.render_to_string(
          'emails/account_verification_email.html', {'user': user,},
        )
        send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)
        data['verification_sent'] = True
      else:
        data['account_is_verified'] = True;
    else:
      data['email_not_found'] = True
  else:
    data['show_verification_form'] = True
  return render(request, pages_dir + 'resend-verification.html', data)