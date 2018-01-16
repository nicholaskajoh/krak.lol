from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.timezone import now


class Post(models.Model):
  title = models.CharField(max_length=150)
  content = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  featured_image = models.ImageField(upload_to="img/posts/", blank=True)
  author = models.ForeignKey(User, related_name='post_author', on_delete=models.CASCADE)
  url = models.CharField(max_length=100)

  def get_comments(self):
    comments = Comment.objects.filter(post=self).order_by('-created_at')
    return comments

  def get_likes(self):
    likes = Like.objects.filter(item_type='post').filter(item_id=self.id)
    return likes

  # Override models save method:
  def save(self, *args, **kwargs):
    if not self.id:
      # generate post url when post is created
      # post url must be unique
      self.url = '/p/' + get_random_string(length=16) + '/'
      while Post.objects.filter(url=self.url).exists():
        self.url = '/p/' + get_random_string(length=16) + '/'
    # delete previous featured_image if exists
    try:
      post = Post.objects.get(id=self.id)
      if post.featured_image != self.featured_image:
        post.featured_image.delete(save=False)
    except: pass
    super(Post, self).save(*args, **kwargs)

  def __str__(self):
    return self.title

@receiver(pre_delete, sender=Post)
def delete_post_featured_image(sender, instance, **kwargs):
  # Pass false so ImageField doesn't save the model.
  instance.featured_image.delete(False)


class Profile(models.Model):
  user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
  full_name = models.CharField(max_length=50, blank=True)
  bio = models.CharField(max_length=200, blank=True)
  link = models.URLField(max_length=150, blank=True)
  profile_photo = models.ImageField(upload_to="img/users/", blank=True)
  following = models.ManyToManyField(User, related_name='user_following', blank=True)
  followers = models.ManyToManyField(User, related_name='user_followers', blank=True)
  url = models.CharField(max_length=100)
  is_verified = models.BooleanField(default=False)
  last_seen = models.DateTimeField(default=now)

  def get_posts(self):
    posts = Post.objects.filter(author=self.user).order_by('-created_at')
    return posts

  # Override models save method:
  def save(self, *args, **kwargs):
    if not self.id:
      # generate profile url when profile is created
      self.url = '/@' + self.user.username + '/'
    # delete previous profile_photo if exists
    try:
      profile = Profile.objects.get(id=self.id)
      if profile.profile_photo != self.profile_photo:
        profile.profile_photo.delete(save=False)
    except: pass
    super(Profile, self).save(*args, **kwargs)

  def __str__(self):
    return self.full_name + ' @' + self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()


class Comment(models.Model):
  content = models.CharField(max_length=250)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)
  author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def get_likes(self):
    likes = Like.objects.filter(item_type='comment').filter(item_id=self.id)
    return likes

  def __str__(self):
    return self.content


class Like(models.Model):
  item_id = models.IntegerField() # ForeignKey: either Post or Comment ID
  ITEM_TYPE_CHOICES = (
    ('post', 'Post'),
    ('comment', 'Comment'),
  )
  item_type = models.CharField(max_length=7, choices=ITEM_TYPE_CHOICES)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username + ', ' + self.item_type


class Notification(models.Model):
  actor_id = models.IntegerField()
  ACTOR_TYPE_CHOICES = (
    ('user', 'User'),
  )
  actor_type = models.CharField(max_length=30, choices=ACTOR_TYPE_CHOICES)
  VERB_TYPES = (
    ('like', 'Like'),
    ('post', 'Post'),
    ('follow', 'Follow'),
    ('comment', 'Comment'),
  )
  verb = models.CharField(max_length=30, choices=VERB_TYPES)
  object_id = models.IntegerField()
  OBJECT_TYPE_CHOICES = (
    ('post', 'Post'),
    ('comment', 'Comment'),
  )
  object_type = models.CharField(max_length=30, choices=OBJECT_TYPE_CHOICES)
  target_id = models.IntegerField()
  TARGET_TYPE_CHOICES = (
    ('user', 'User'),
  )
  target_type = models.CharField(max_length=30, choices=TARGET_TYPE_CHOICES)
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return "[{0}] actor({1}, {2}), object({3}, {4}), target({5}, {6})".format(
      self.verb,
      self.actor_type,
      self.actor_id,
      self.object_type,
      self.object_id,
      self.target_type,
      self.target_id
    )