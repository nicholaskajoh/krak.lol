# Krak template tags and filters

# from .collections import Collections
from django import template
from social.models import Notification, Like

register = template.Library()
data = {}

@register.inclusion_tag('social/header.html')
def header(current_user):
	# populate sidebar with dynamic data for all views
	if current_user.is_authenticated():
		notifs = Notification.objects.filter(target_type="user", target_id=current_user.id, is_read=False).count()
		data['notifs'] = notifs
		pass
	data['current_user'] = current_user
	return data

@register.inclusion_tag('social/partials/latest-comment.html')
def get_latest_comment(post, current_user):
	comment = post.get_comments().latest('created_at')
	data['comment'] = comment
	data['current_user'] = current_user
	return data

# determine if a post has been liked by the current user or not
@register.filter(name='post_liked')
def post_liked(post, user):
	if user.is_authenticated():
		return Like.objects.filter(item_id=post.id, item_type='post', user=user).exists()
	return False

# determine if a comment has been liked by the current user or not
@register.filter(name='comment_liked')
def comment_liked(comment, user):
	if user.is_authenticated():
		return Like.objects.filter(item_id=comment.id, item_type='comment', user=user).exists()
	return False

# determine if a user has been followed by the current user or not
@register.filter(name='user_followed')
def user_followed(user, current_user):
	return user.profile.followers.filter(pk=current_user.id).exists()

# UTIL

# get the number of posts a user has based on the current user
@register.filter(name='get_user_posts_count')
def get_user_posts_count(user, current_user):
	return user.profile.get_posts().count()

# return number of characters (int) in a string
@register.filter(name='num_chars')
def num_chars(string):
	return len(string)