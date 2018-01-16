from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.home, name='home'),
	url(r'^explore/popular/$', views.explore_posts, name='explore_posts'),
	url(r'^explore/people/$', views.explore_users, name='explore_users'),
	url(r'^post/$', views.post, name='post'), # create/edit post
    url(r'^(?P<username>@[a-zA-Z0-9_.]+)/$', views.users, name='user_profile'), # user profile
    url(r'^(?P<username>@[a-zA-Z0-9_.]+)/(?P<page>[a-z]+)/$', views.users, name='user_pages'),
    url(r'^edit-profile/$', views.edit_profile, name='edit_profile'),
	url(r'^notifications/$', views.notifications, name='notifications'),
	url(r'^p/(?P<url>[a-zA-Z0-9]+)/$', views.posts, name='posts'),
	url(r'^settings/$', views.user_settings, name='settings'), # settings
	url(r'^search/$', views.search, name='search'),
	url(r'^tagged/(?P<tag>[a-zA-Z0-9_]+)/$', views.search, name='tagged'),

	# auth
	url(r'^auth/$', views.auth, name='auth'),
	url(r'^logout/$', views.logout, name='logout'),

	# password reset
	url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # verify account email
    url(r'^verify/$', views.verify, name='verify_account'),
    url(r'^resend-verification/$', views.resend_verification, name='resend_verification'),

	# AJAX
	url(r'^like/$', views.like, name='like'),
	url(r'^follow/$', views.follow, name='follow'),
	url(r'^delete/$', views.delete, name='delete'),
	url(r'^comment/$', views.comment, name='comment'),
	url(r'^load-comments/$', views.load_comments, name='load_comments'),
	url(r'^clear-image/$', views.clear_image, name='clear_image'),
	url(r'^load-user-lists/$', views.load_user_lists, name='load_user_lists'),
	url(r'^load-feeds/$', views.load_feeds, name='load_feeds'),
	url(r'^load-popular/$', views.load_popular, name='load_popular'),
	url(r'^load-users/$', views.load_users, name='load_users'),
	url(r'^load-search-results/$', views.load_search_results, name='load_search_results'),
	url(r'^load-notifications/$', views.load_notifications, name='load_notifications'),
]

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)