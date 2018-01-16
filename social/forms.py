import os.path
from django import forms
from django.forms import ModelForm
from .models import Post, Profile, Comment
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup
import re

class SignUpForm(ModelForm):
	def __init__(self, *args, **kwargs):
		# first call parent's constructor
		super(SignUpForm, self).__init__(*args, **kwargs)
		# there's a 'fields' property now
		self.fields['username'].validators.append(
			RegexValidator(
				regex='^[a-zA-Z][a-zA-Z0-9_.]+$',
				message='Only alphabets, numbers, _ and . are allowed for usernames. Your username must start with an alphabet.',
				code='invalid_username',
			)
		)
		self.fields['email'].required = True

	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		error_messages = {
			'username': {
				'required': 'A username is required.',
			},
			'email': {
				'required': 'An email address is required.',
			},
			'password': {
				'required': 'A password is required.',
			},
		}

	def clean(self):
		cleaned_data = super(SignUpForm, self).clean()

		username = cleaned_data.get("username")
		email = cleaned_data.get("email")

		# disallow blacklisted names as username
		# username blacklist file
		with open(os.path.dirname(__file__) + '/username_blacklist.txt') as ub_file:
			username_blacklist = ub_file.read().splitlines()
		# username must not be in username blacklist
		if username in username_blacklist:
			raise ValidationError("The username you've chosen is not allowed! Please use another.")

		# email must be unique
		# NB: users w/o emails have their email field as empty string
		if User.objects.filter(email=email).exists() and email != "":
			raise ValidationError("A user with that email address already exists.")

		return cleaned_data


class PostForm(ModelForm):
	has_featured_image = forms.BooleanField(required=False, widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		modelchoicefields = [field for field_name, field in self.fields.items() if isinstance(field, forms.ModelChoiceField)]

		for field in modelchoicefields:
			field.empty_label = None

	class Meta:
		model = Post
		fields = ['title', 'content', 'featured_image']
		# widgets = {'content': forms.HiddenInput()}
		error_messages = {
			'title': {
				'required': 'Your post definitely needs a title!',
			},
		}

	def clean(self):
		cleaned_data = super(PostForm, self).clean()

		content = cleaned_data.get("content")
		featured_image = cleaned_data.get("featured_image")
		# check if a featured image has already been uploaded for this post
		# if so, allow user to submit form without image even if content field is empty
		has_featured_image = cleaned_data.get("has_featured_image")

		if not (content or featured_image or has_featured_image):
			raise ValidationError("You must add (at least) some content or a featured image to your post!")

		return cleaned_data

	def clean_content(self):
		content = self.cleaned_data.get("content")

		# sanitize data with BeautifulSoup
		content = BeautifulSoup('<div>' + content + '</div>', "html.parser")
		tag_blacklist = ['script', 'style']
		# extract blacklist tags and contents
		for tag in tag_blacklist:
			for x in content.find_all(tag):
				x.extract()
		content = str(content.div)
		# remove wrapping divs
		content = re.sub(r'<(div|\/div)>', '', content, flags=re.IGNORECASE)
		self.data["content"] = content

		return content


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class EditProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['full_name', 'bio', 'link', 'profile_photo']