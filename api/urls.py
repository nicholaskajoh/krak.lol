from django.conf.urls import url
from api import views
from rest_framework.authtoken.views import obtain_auth_token
 
urlpatterns = [
  # auth
  url(r'^token-auth/$', obtain_auth_token),
  
  # posts
  url(r'^new-post/$', views.NewPost.as_view(), name='new_post'),
  url(r'^post/(?P<pk>[0-9]+)/$', views.Post.as_view(), name='post'),
  url(r'^post/(?P<pk>[0-9]+)/comments/(?P<page>[0-9]+)/$', views.Comments.as_view(), name='post_comments'),
  url(r'^feed/(?P<page>[0-9]+)/$', views.Feed.as_view(), name='feed'),
  url(r'^popular-posts/(?P<page>[0-9]+)/$', views.PopularPosts.as_view(), name='popular_posts'),

  # comments
  url(r'^new-comment/(?P<post_id>[0-9]+)/$', views.NewComment.as_view(), name='new_comment'),
  url(r'^comment/(?P<pk>[0-9]+)/$', views.Comment.as_view(), name='comment'),

  # users
  url(r'^user/(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), name='user_profile'),
  url(r'^user/(?P<pk>[0-9]+)/posts/(?P<page>[0-9]+)/$', views.UserPosts.as_view(), name='user_posts'),
  url(r'^user/liked/(?P<page>[0-9]+)/$', views.UserLikedPosts.as_view(), name='user_liked_posts'),
  url(r'^user/(?P<pk>[0-9]+)/following/(?P<page>[0-9]+)/$', views.UserFollowing.as_view(), name='user_following'),
  url(r'^user/(?P<pk>[0-9]+)/followers/(?P<page>[0-9]+)/$', views.UserFollowers.as_view(), name='user_followers'),
  url(r'^popular-users/(?P<page>[0-9]+)/$', views.PopularUsers.as_view(), name='popular_users'),

  # search
  url(r'^search/$', views.Search.as_view(), name='search'),
  url(r'^tagged/(?P<tag>[a-zA-Z0-9_]+)/$', views.Search.as_view(), name='tagged'),

  # other
  url(r'^like/$', views.Like.as_view(), name='like'),
  url(r'^follow/$', views.Follow.as_view(), name='follow'),
  url(r'^clear-image/$', views.ClearImage.as_view(), name='clear_image'),
  url(r'^notifications/(?P<page>[0-9]+)/$', views.Notifications.as_view(), name='notifications'),
]