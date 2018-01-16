# views for various auth functionality

from django.contrib import messages
from social.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.core.mail import send_mail

pages_dir = 'social/pages/'

def auth(request):
  template = pages_dir + 'auth.html'
  data = {}

  # login or register
  if request.method == 'POST':
    action = request.POST.get('action') # login or register
    redirect_url = request.POST.get('redirect_url')
    # login
    if action == 'login':
      username = request.POST.get('username', '').lower()
      password = request.POST.get('password', '')
      user = authenticate(username=username, password=password)
      errors = []
      if user is not None:
        if not user.is_active: # suspended user
          errors.append('Your account has been suspended. Please contact us (@krak_lol on Twitter or Instagram) for more information.')
        elif not user.profile.is_verified: # unverified account
          errors.append('Your account has not yet been verified! Please check your inbox for a verification email. Didn\'t get one? <a href="/resend-verification">Click here to receive another.</a>')
        else:
          # correct password
          auth_login(request, user)
          errors = False
          # redirect url
          data['next'] = redirect_url
      else:
        # invalid username or password
        errors.append('Invalid username, email or password!')
      data['errors'] = errors
      return JsonResponse(data)
    # register
    elif action == 'register':
      form = SignUpForm(request.POST)
      if form.is_valid():
        username = form.cleaned_data['username'].lower()
        email = form.cleaned_data['email'].lower()

        # create user
        user = User(username=username, email=email)
        user.set_password(form.cleaned_data['password'])
        user.save()

        # send user account verification email
        subject = 'Verify Your Krak.lol Account'
        message = ''
        from_email = 'noreply@krak.lol'
        recipient_list = (form.cleaned_data['email'],)
        html_message = loader.render_to_string(
          'emails/account_verification_email.html', {'user': user,},
        )
        send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)

        # log user in
        user = authenticate(username=username, password=form.cleaned_data['password'])
        auth_login(request, user)

        # verification message
        messages.info(request, "Hi @"+user.username+", we just mailed you an account verification link. Thanks for joining our community. Have fun!!!")

        data['errors'] = False
        # redirect url
        data['next'] = '/@'+user.username+'/'
      else:
        data['errors'] = form.errors
      return JsonResponse(data)

  # GET request
  return HttpResponseRedirect("/")


def logout(request):
  auth_logout(request)
  return HttpResponseRedirect("/")