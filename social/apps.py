from __future__ import unicode_literals

from django.apps import AppConfig
from watson import search as watson

class SocialConfig(AppConfig):
	name = 'social'
	def ready(self):
		Post = self.get_model("Post")
		Profile = self.get_model("Profile")

		watson.register(
			Post, 
			PostSearchAdapter, 
			store=('url',)
		)
		watson.register(
			Profile, 
			ProfileSearchAdapter, 
			fields=('user__username', 'full_name', 'bio',), 
			store=('url',)
		)

# SearchAdapter subclasses
class PostSearchAdapter(watson.SearchAdapter):
	def get_description(self, obj):
		return obj.content

class ProfileSearchAdapter(watson.SearchAdapter):
	def get_description(self, obj):
		return obj.bio