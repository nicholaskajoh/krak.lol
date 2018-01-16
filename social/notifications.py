from django.contrib.auth.models import User
from social.models import Post, Comment

# Notifications builder for Krak.lol
class Notify:
  # build notification
  def __init__(self, notif, return_dict=False):
    self.return_dict = return_dict
    self.notif_dict = { 'verb': notif.verb, 'created_at': notif.created_at }

    # get actor
    if notif.actor_type == "user":
      user = User.objects.get(id=notif.actor_id)
      self.actor_name = user.username
      self.actor_url = user.profile.url

    # get object
    if notif.object_type == "post":
      post = Post.objects.get(id=notif.object_id)
      self.object_name = post.title
      self.object_type = "post"
      self.object_url = post.url
    elif notif.object_type == "comment":
      comment = Comment.objects.get(id=notif.object_id)
      self.object_name = (comment.content[:50] + '...') if len(comment.content) > 50 else comment.content
      self.object_type = "comment"
      self.object_url = "#"
      # other
      self.comment_post_title = comment.post.title
      self.comment_post_url = comment.post.url

    # get target
    if notif.target_type == "user":
      user = User.objects.get(id=notif.target_id)
      self.target_name = user.username
      self.target_url = user.profile.url

    # set notif string
    if notif.verb == "like":
      self.n_like()
    elif notif.verb == "follow":
      self.n_follow()
    elif notif.verb == "comment":
      self.n_comment()

    # new label for unread notifications
    if not notif.is_read:
      if self.return_dict:
        self.notif_dict["is_new"] = True
      else:
        self.notif_string += ' <span class="label label-primary">New</span>'

  # return notification string/html or dictionary
  def get(self):
    if self.return_dict:
      return self.notif_dict
    else:
      return self.notif_string

  # STRING BUILDERS FOR NOTIFICATION VERBS
  def n_like(self):
    self.notif_dict.update({
      'verb': "like",
      'actor_url': self.actor_url,
      'actor_name': self.actor_name,
      'object_type': self.object_type,
      'object_url': self.object_url,
      'object_name': self.object_name
    })

    self.notif_string = '<a href="{0}">@{1}</a> liked your {2} <a href="{3}">"{4}"</a>.'.format(
      self.notif_dict['actor_url'],
      self.notif_dict['actor_name'],
      self.notif_dict['object_type'],
      self.notif_dict['object_url'],
      self.notif_dict['object_name']
    )

  def n_follow(self):
    self.notif_dict.update({
      'actor_url': self.actor_url,
      'actor_name': self.actor_name
    })

    self.notif_string = '<a href="{0}">@{1}</a> started following you.'.format(
      self.notif_dict['actor_url'],
      self.notif_dict['actor_name']
    )

  def n_comment(self):
    self.notif_dict.update({
      'actor_url': self.actor_url,
      'actor_name': self.actor_name,
      'object_name': self.object_name,
      'comment_post_url': self.comment_post_url,
      'comment_post_title': self.comment_post_title
    })

    self.notif_string = '<a href="{0}">@{1}</a> commented "{2}" on your post <a href="{3}">"{4}"</a>.'.format(
      self.notif_dict['actor_url'],
      self.notif_dict['actor_name'],
      self.notif_dict['object_name'],
      self.notif_dict['comment_post_url'],
      self.notif_dict['comment_post_title']
    )