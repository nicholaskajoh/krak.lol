from social.models import Post, Profile, Comment
from django.contrib.auth.models import User
from watson.models import SearchEntry
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
  following_count = serializers.IntegerField(source='following.count', read_only=True)
  followers_count = serializers.IntegerField(source='followers.count', read_only=True)
  posts_count = serializers.IntegerField(source='get_posts.count', read_only=True)

  class Meta:
    model = Profile
    fields = ('id', 'full_name', 'bio', 'profile_photo', 'following_count', 'followers_count', 'posts_count')
    read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
  profile = UserProfileSerializer()

  class Meta:
    model = User
    fields = ('id', 'username', 'profile')
    read_only_fields = ('id', 'username')


class FullUserSerializer(serializers.ModelSerializer):
  profile = UserProfileSerializer()

  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'profile')
    read_only_fields = ('id', )


class PostSerializer(serializers.ModelSerializer):
  author = UserSerializer()
  likes_count = serializers.IntegerField(source='get_likes.count', read_only=True)
  comments_count = serializers.IntegerField(source='get_comments.count', read_only=True)

  class Meta:
    model = Post
    fields = ('id', 'title', 'content', 'created_at', 'featured_image', 'author', 'url', 'likes_count', 'comments_count')
    read_only_fields = ('id', 'author', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer()
  
  class Meta:
    model = Comment
    fields = ('id', 'content', 'author', 'created_at')
    read_only_fields = ('id', 'author', 'created_at')


class SearchEntrySerializer(serializers.ModelSerializer):
  url = serializers.CharField(source='meta.url', read_only=True)

  class Meta:
    model = SearchEntry
    fields = ('title', 'description', 'url')