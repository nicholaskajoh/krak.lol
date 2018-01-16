from django.contrib.auth.models import User
from social.models import Post, Notification

from datetime import datetime, timedelta
from django.utils import timezone

from django.template import loader
from django.core.mail import send_mail

def login_to_site():
  # email reminders to users who've not logged in for a while
  a_week_ago = timezone.now() - timedelta(days=7)
  users = User.objects.all()
  for user in users:
    if user.profile.last_seen <= a_week_ago:
      # send mail
      subject = "It's Been a Little While Since We've Seen You" 
      message = ''
      from_email = 'noreply@krak.lol'
      recipient_list = (user.email,)
      html_message = loader.render_to_string(
        'emails/login_to_site_email.html', {'user': user,},
      )
      send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)

def make_first_post():
  # email reminders to users who've not made a post yet
  users = User.objects.all()
  for user in users:
    if Post.objects.filter(author=user).count() == 0:
      # send mail
      subject = 'Make Your First Post on Krak.lol'
      message = ''
      from_email = 'noreply@krak.lol'
      recipient_list = (user.email,)
      html_message = loader.render_to_string(
        'emails/make_first_post_email.html', {'user': user,},
      )
      send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)

def account_notifications():
  # inform users of their account notifications if any
  users = User.objects.all()
  for user in users:
    notifs_count = Notification.objects.filter(target_type="user", target_id=user.id, is_read=False).count()
    if notifs_count > 0:
      # send mail
      subject = 'You Have ' + str(notifs_count) + ' New Notifications'
      message = ''
      from_email = 'noreply@krak.lol'
      recipient_list = (user.email,)
      html_message = loader.render_to_string(
        'emails/account_notifications_email.html', {'user': user,},
      )
      send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)

def connect_with_others():
  # encourage users who have less than 10 followers
  # to connect with others i.e follow etc
  users = User.objects.all()
  for user in users:
    if user.profile.followers.count() < 10:
      # send mail
      subject = 'Connect with Others on Krak.lol'
      message = ''
      from_email = 'noreply@krak.lol'
      recipient_list = (user.email,)
      html_message = loader.render_to_string(
        'emails/connect_with_others_email.html', {'user': user,},
      )
      send_mail(subject, message, from_email, recipient_list, fail_silently=True, html_message=html_message)