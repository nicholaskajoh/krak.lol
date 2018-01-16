import calendar
from datetime import datetime, timedelta
from social.models import Post, Like
from django.contrib.auth.models import User
from django.db.models import Q

# This class preprocesses and returns different collections
class Collections:

  # get new posts
  def feed(self, current_user):
    # Obtained by selecting the best most recent posts (in the last 30 days) of users the current user is following

    # threshold of 30 days
    post_time_threshold = datetime.now() - timedelta(days=30)

    # get ids of users the current user is following
    following = current_user.profile.following.all()
    ids = []
    for i in following:
      ids.append(i.id) # put the ids in a list

    # get posts by these users
    new_posts = Post.objects.filter(author__in=ids)
    new_posts = new_posts.filter(created_at__gte=post_time_threshold)
    # sort the posts by likes and datetime
    # preference goes to recent posts with more likes
    new_posts = sorted(
      new_posts, 
      key=lambda p: (86400 * p.get_likes().count()) + calendar.timegm(p.created_at.utctimetuple()), 
      reverse=True
    )

    return new_posts[:100]

  # get popular posts
  def popular(self, current_user):
    # obtained by selecting the best posts in the last 90 days

    # threshold of 90 days
    post_time_threshold = datetime.now() - timedelta(days=90)

    popular_posts = Post.objects.filter(created_at__gte=post_time_threshold)
    # exclude posts by users the current user is following 
    if current_user.is_authenticated():
      # get ids of users the current user is following
      following = current_user.profile.following.all()
      ids = []
      for i in following:
        ids.append(i.id) # put the ids in a list
      popular_posts = popular_posts.exclude(author__in=ids)
    # sort posts by likes and datetime
    # preference goes to recent posts with more likes
    popular_posts = sorted(
      popular_posts, 
      key=lambda p: (86400 * p.get_likes().count()) + calendar.timegm(p.created_at.utctimetuple()), 
      reverse=True
    )

    return popular_posts[:100]

  # get posts liked by a user
  def liked(self, current_user):
    # get user post likes
    likes = Like.objects.filter(item_type="post", user=current_user)
    ids = []
    for i in likes:
      ids.append(i.item_id)

    # get liked posts
    liked_posts = Post.objects.filter(pk__in=ids).order_by('-created_at')

    return liked_posts

  # get popular users
  def popular_users(self, current_user):
    # obtained by selecting the most popular users
    users = User.objects.all()
    if current_user.is_authenticated():
      # exclude current user and other users they follow
      users = users.exclude(profile__user=current_user)
      users = users.exclude(profile__followers=current_user)
    # sort users by posts, likes and followers
    # preference goes to users with more posts, likes and followers
    users = sorted(
      users, 
      key=lambda u: len(u.profile.get_posts()) + (3 * u.profile.followers.count()),
      reverse=True
    )

    return users[:100]

  # get other posts related to a given post
  def related_posts(self, post, limit=5):
    # uses popular posts in the krak that post is in
    related_posts = Post.objects.filter(krak=post.krak).exclude(id=post.id)
    # sort posts by likes and datetime
    # preference goes to recent posts with more likes
    related_posts = sorted(
      related_posts, 
      key=lambda p: (86400 * p.get_likes().count()) + calendar.timegm(p.created_at.utctimetuple()), 
      reverse=True
    )
    return related_posts[:limit]