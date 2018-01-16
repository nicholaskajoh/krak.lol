from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.contrib.auth.models import User as UserModel
from social.models import Post as PostModel, Comment as CommentModel, Notification as NotifModel, Like as LikeModel
from api.serializers import PostSerializer, UserSerializer, CommentSerializer, SearchEntrySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.collections import Collections
from social.forms import PostForm, CommentForm
from watson import search as watson
from social.notifications import Notify


c = Collections()

def paginate(input_list, page, results_per_page=10):
  paginator = Paginator(input_list, results_per_page)
  try:
    output_list = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver 1st page.
    output_list = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), return empty list
    output_list = []
  return output_list

class Feed(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request, page=1, format=None):
    posts = c.feed(request.user)
    posts = paginate(posts, page, 15)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class PopularPosts(APIView):
  def get(self, request, page=1, format=None):
    posts = c.popular(request.user)
    posts = paginate(posts, page, 15)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class PopularUsers(APIView):
  def get(self, request, page=1, format=None):
    users = c.popular_users(request.user)
    users = paginate(users, page, 15)
    serializer =  UserSerializer(users, many=True)
    return Response(serializer.data)


class NewPost(APIView):
  permission_classes = (IsAuthenticated, )

  def post(self, request, format=None):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = PostModel()
      post.title = request.POST.get('title')
      post.content = request.POST.get('content')
      post.author = request.user
      # add image if uploaded
      featured_image = request.FILES.get('featured_image', False)
      if featured_image:
        post.featured_image = featured_image
      post.save()
      serializer = PostSerializer(post)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class Post(APIView):
  permission_classes = (IsAuthenticatedOrReadOnly, )

  def get_post(self, pk):
    try:
      return PostModel.objects.get(pk=pk)
    except PostModel.DoesNotExist:
      raise Http404("Post does not exist!")

  # single post
  def get(self, request, pk, format=None):
    post = self.get_post(pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

  # update post
  def put(self, request, pk, format=None):
    post = self.get_post(pk)
    if request.user == post.author:
      form = PostForm(request.POST, request.FILES)
      if form.is_valid():
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        # add image if uploaded
        featured_image = request.FILES.get('featured_image', False)
        if featured_image:
          post.featured_image = featured_image
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

  # delete post
  def delete(self, request, pk, format=None):
    post = self.get_post(pk)
    if request.user == post.author:
      # delete notifications associated with this post
      try:
        NotifModel.objects.filter(
          object_id=post.id,
          object_type="post"
        ).delete()
      except NotifModel.DoesNotExist:
        pass
      # delete the post
      post.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)


class NewComment(APIView):
  permission_classes = (IsAuthenticated, )

  def post(self, request, post_id, format=None):
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = CommentModel()
      comment.content = request.POST.get('content')
      comment.post = PostModel.objects.get(id=post_id)
      comment.author = request.user
      comment.save()
      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
  permission_classes = (IsAuthenticatedOrReadOnly, )

  def get_comment(self, pk):
    try:
      return CommentModel.objects.get(pk=pk)
    except CommentModel.DoesNotExist:
      raise Http404("Comment does not exist!")

  # single post
  def get(self, request, pk, page=1, format=None):
    comment = self.get_comment(pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

  # update comment
  def put(self, request, pk, format=None):
    comment = self.get_comment(pk)
    if request.user == comment.author:
      form = CommentForm(request.POST)
      if form.is_valid():
        comment.content = request.POST.get('content')
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

  # delete comment
  def delete(self, request, pk, format=None):
    comment = self.get_comment(pk)
    if request.user == comment.author:
      # delete notifications associated with this comment
      try:
        NotifModel.objects.get(
          object_id=comment.id,
          object_type="comment"
        ).delete()
      except NotifModel.DoesNotExist:
          pass
      # delete the comment
      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)


class Comments(APIView):
  # comments for a post
  def get(self, request, pk, page=1, format=None):
    try:
      comments = PostModel.objects.get(pk=pk).get_comments()
    except CommentModel.DoesNotExist:
      raise Http404("Post does not exist!")
    comments = paginate(comments, page, 15)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


class UserProfile(APIView):
  def get(self, request, pk, format=None):
    try:
      user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
      raise Http404("User does not exist!")
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserPosts(APIView):
  def get(self, request, pk, page=1, format=None):
    try:
      user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
      raise Http404("User does not exist!")
    posts = user.profile.get_posts()
    posts = paginate(posts, page, 15)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class UserLikedPosts(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request, page=1, format=None):
    posts = c.liked(request.user)
    posts = paginate(posts, page, 15)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class UserFollowing(APIView):
  def get(self, request, pk, page=1, format=None):
    try:
      user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
      raise Http404("User does not exist!")
    following = user.profile.following.all()
    following = paginate(following, page, 15)
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)


class UserFollowers(APIView):
  def get(self, request, pk, page=1, format=None):
    try:
      user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
      raise Http404("User does not exist!")
    followers = user.profile.followers.all()
    followers = paginate(followers, page, 15)
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)


class Notifications(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request, page=1, format=None):
    notifs = NotifModel.objects.filter(target_type="user", target_id=request.user.id).order_by('-created_at')
    notifs = paginate(notifs, page, 10)
    notifications = []
    for n in notifs:
      notif = Notify(n, True)
      notification = notif.get()
      notifications.append(notification)
      # mark unread notification as read
      if n.is_read == False:
        n.is_read = True
        n.save()
    return Response(notifications)



class Like(APIView):
  permission_classes = (IsAuthenticated, )

  def get_liked_object(self, item_id, item_type):
    if item_type == "post":
      liked_object = PostModel.objects.get(id=item_id)
    elif item_type == "comment":
      liked_object = CommentModel.objects.get(id=item_id)
    return liked_object

  def post(self, request, format=None):
    item_id = request.POST.get('itemId')
    item_type = request.POST.get('itemType')
    # notification data
    liked_object = self.get_liked_object(item_id, item_type)
    target = liked_object.author if item_type != "user" else liked_object
    # CREATE OR DELETE LIKE
    like = LikeModel.objects.filter(item_id=item_id, item_type=item_type, user=request.user)
    if like.exists():
      # UNLIKE
      like.delete()
      # delete notification
      try:
        NotifModel.objects.get(
          actor_id=request.user.id,
          actor_type="user",
          verb="like",
          object_id=liked_object.id,
          object_type=item_type,
          target_id=target.id,
          target_type="user"
        ).delete()
      except NotifModel.DoesNotExist:
        pass
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      # LIKE
      like = LikeModel.objects.create(item_id=item_id, item_type=item_type, user=request.user)
      # create notification
      # NB: users should not be notified of their actions on objects they created
      if like.user != target:
        NotifModel.objects.create(
          actor_id=request.user.id,
          actor_type="user",
          verb="like",
          object_id=liked_object.id,
          object_type=item_type,
          target_id=target.id,
          target_type="user"
        )
      return Response(status=status.HTTP_201_CREATED)


class Follow(APIView):
  permission_classes = (IsAuthenticated, )

  def post(self, request, format=None):
    action = request.POST.get('action') # follow/unfollow
    followed_user_id = request.POST.get('followedUserId')
    followed_user = UserModel.objects.get(id=followed_user_id)

    # users cannot follow themselves
    if followed_user == request.user:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    if action == "follow":
      followed_user.profile.followers.add(request.user)
      request.user.profile.following.add(followed_user)
      # create notification
      NotifModel.objects.create(
        actor_id=request.user.id,
        actor_type="user",
        verb="follow",
        object_id=followed_user.id,
        object_type="user",
        target_id=followed_user.id,
        target_type="user"
      )
      return Response(status=status.HTTP_201_CREATED)
    elif action == "unfollow":
      followed_user.profile.followers.remove(request.user)
      request.user.profile.following.remove(followed_user)
      try:
        NotifModel.objects.filter(
          actor_id=request.user.id,
          actor_type="user",
          verb="follow",
          object_id=followed_user.id,
          object_type="user",
          target_id=followed_user.id,
          target_type="user"
        ).delete()
      except NotifModel.DoesNotExist:
        pass
      return Response(status=status.HTTP_204_NO_CONTENT)


class ClearImage(APIView):
  permission_classes = (IsAuthenticated, )

  def post(self, request, format=None):
    item_id = int(request.POST.get('itemId'))
    item_type = request.POST.get('itemType')

    if item_type == 'post':
      PostModel.objects.get(id=item_id, author=request.user).featured_image.delete(save=True)
      return Response(status=status.HTTP_204_NO_CONTENT)
    elif item_type == 'user' and item_id == request.user.id:
      UserModel.objects.get(id=item_id).profile.profile_photo.delete(save=True)
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class Search(APIView):
  def get(self, request, tag=None, page=1, format=None):
    q = request.GET.get('q', '') if tag == None else tag
    if q != '':
      results = watson.search(q)
      results = paginate(results, page, 15)
      serializer = SearchEntrySerializer(results, many=True)
      return Response(serializer.data)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
