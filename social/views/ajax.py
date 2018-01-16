# views which respond to ajax requests

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from social.models import Like, Post, Comment, Notification
from social.notifications import Notify
from social.forms import CommentForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.collections import Collections
from watson import search as watson

c = Collections()
data = {}

# like or unlike posts, kraks, users or comments
def like(request):
    item_id = request.POST.get('itemId')
    item_type = request.POST.get('itemType')

    # get notification data
    if item_type == "post":
        liked_object = Post.objects.get(id=item_id)
    elif item_type == "comment":
        liked_object = Comment.objects.get(id=item_id)
    target = liked_object.author if item_type != "user" else liked_object

    # user must be authenticated to like/unlike
    if request.user.is_authenticated:
        like = Like.objects.filter(item_id=item_id, item_type=item_type, user=request.user)
        if like.exists():
            # unlike
            like.delete()
            # delete notification
            try:
                Notification.objects.get(
                    actor_id=request.user.id,
                    actor_type="user",
                    verb="like",
                    object_id=liked_object.id,
                    object_type=item_type,
                    target_id=target.id,
                    target_type="user"
                ).delete()
            except Notification.DoesNotExist:
                pass
        else:
            # like
            like = Like.objects.create(item_id=item_id, item_type=item_type, user=request.user)
            # create notification
            # NB: users should not be notified of their actions on objects they created
            if like.user != target:
                Notification.objects.create(
                    actor_id=request.user.id,
                    actor_type="user",
                    verb="like",
                    object_id=liked_object.id,
                    object_type=item_type,
                    target_id=target.id,
                    target_type="user"
                )
        data['auth'] = True
    else: # anonymous user
        data['auth'] = False
    return JsonResponse(data)


# follow or unfollow users
def follow(request):
    action = request.POST.get('action') # follow/unfollow
    followed_user_id = request.POST.get('followedUserId')
    followed_user = User.objects.get(id=followed_user_id)

    # users cannot follow themselves
    if followed_user == request.user:
        return JsonResponse({})

    # user must be authenticated to follow/unfollow
    if request.user.is_authenticated():
        if action == 'follow':
            followed_user.profile.followers.add(request.user)
            request.user.profile.following.add(followed_user)
            # create notification
            Notification.objects.create(
                actor_id=request.user.id,
                actor_type="user",
                verb="follow",
                object_id=followed_user.id,
                object_type="user",
                target_id=followed_user.id,
                target_type="user"
            )
        elif action == 'unfollow':
            followed_user.profile.followers.remove(request.user)
            request.user.profile.following.remove(followed_user)
            try:
                Notification.objects.get(
                    actor_id=request.user.id,
                    actor_type="user",
                    verb="follow",
                    object_id=followed_user.id,
                    object_type="user",
                    target_id=followed_user.id,
                    target_type="user"
                ).delete()
            except Notification.DoesNotExist:
                pass
        data['auth'] = True
    else:
        data['auth'] = False
    return JsonResponse(data)


def delete(request):
    item_id = request.POST.get('itemId')
    item_type = request.POST.get('itemType')

    if item_type == 'post':
        item = Post.objects.get(id=item_id)
        messages.success(request, "Post deleted successfully!")
        # delete notifications associated with this post
        try:
            Notification.objects.filter(
                object_id=item.id,
                object_type="post"
            ).delete()
        except Notification.DoesNotExist:
            pass
    elif item_type == 'comment':
        item = Comment.objects.get(id=item_id)
        messages.success(request, "Comment deleted successfully!")
        # delete notifications associated with this comment
        try:
            Notification.objects.get(
                object_id=item.id,
                object_type="comment"
            ).delete()
        except Notification.DoesNotExist:
            pass

    if item.author == request.user:
        item.delete()
        data['error'] = False
    return JsonResponse(data)


def comment(request):
    if request.user.is_authenticated():
        data['auth'] = True;
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            page = request.POST.get('page')
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(content=content, post=post, author=request.user)
            show_comment_actions = True if page == "post" else False 
            comment_html = loader.render_to_string(
                'social/partials/latest-comment.html', {
                    'comment': comment, 
                    'current_user': request.user, 
                    'show_comment_actions': show_comment_actions
                },
            )
            data['comment_html'] = comment_html
            data['errors'] = False
            # create notification
            if post.author != comment.author:
                Notification.objects.create(
                    actor_id=request.user.id,
                    actor_type="user",
                    verb="comment",
                    object_id=comment.id,
                    object_type="comment",
                    target_id=post.author.id,
                    target_type="user"
                )
        else:
            data['errors'] = form.errors
    else:
        data['auth'] = False
        
    return JsonResponse(data)


def clear_image(request):
    item_id = int(request.POST.get('itemId'))
    item_type = request.POST.get('itemType')

    if item_type == 'post':
        Post.objects.get(id=item_id, author=request.user).featured_image.delete(save=True)
    elif item_type == 'user' and item_id == request.user.id:
        User.objects.get(id=item_id).profile.profile_photo.delete(save=True)

    messages.success(request, 'Image successfully removed!')
    return JsonResponse(data)


#### LAZY LOADING ####
######################

# META
def paginate_list(input_list, page, results_per_page=10):
    paginator = Paginator(input_list, results_per_page)
    # paginate
    try:
        output_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver 2nd page.
        output_list = paginator.page(2)
    except EmptyPage:
        # If page is out of range (e.g. 9999), return empty list
        output_list = []
    # push to template
    return output_list


def load_feeds(request):
    page = request.POST.get('page')

    posts = c.feed(request.user)
    posts = paginate_list(posts, page, 15)
    posts_html = loader.render_to_string(
        'social/partials/posts.html',
        {'posts': posts, 'user': request.user, 'MEDIA_URL': settings.MEDIA_URL},
    )
    data['has_next'] = posts.has_next()
    data['list_html'] = posts_html

    return JsonResponse(data)


def load_user_lists(request):
    user_list = request.POST.get('userList') # posts, following, followers, liked posts
    user_id = request.POST.get('userId')
    page = request.POST.get('page')
    user = User.objects.get(id=user_id)

    if user_list == 'posts':
        posts = user.profile.get_posts(request.user)
        posts = paginate_list(posts, page)
        posts_html = loader.render_to_string(
            'social/partials/posts.html',
            {'posts': posts, 'MEDIA_URL': settings.MEDIA_URL},
        )
        data['has_next'] = posts.has_next()
        data['list_html'] = posts_html
    elif user_list == 'following':
        following = list(reversed(user.profile.following.all()))
        following = paginate_list(following, page)
        following_html = loader.render_to_string(
            'social/partials/users.html',
            {'user': request.user, 'users': following, 'MEDIA_URL': settings.MEDIA_URL},
        )
        data['has_next'] = following.has_next()
        data['list_html'] = following_html
    elif user_list == 'followers':
        followers = list(reversed(user.profile.followers.all()))
        followers = paginate_list(followers, page)
        followers_html = loader.render_to_string(
            'social/partials/users.html',
            {'user': request.user, 'users': followers, 'MEDIA_URL': settings.MEDIA_URL},
        )
        data['has_next'] = followers.has_next()
        data['list_html'] = followers_html
    elif user_list == 'liked':
        liked_posts = c.liked(request.user)
        liked_posts = paginate_list(liked_posts, page)
        liked_html = loader.render_to_string(
            'social/partials/posts.html',
            {'posts': liked_posts, 'MEDIA_URL': settings.MEDIA_URL},
        )
        data['has_next'] = liked_posts.has_next()
        data['list_html'] = liked_html
    return JsonResponse(data)

    
def load_comments(request):
    post_id = request.POST.get('postId')
    page = request.POST.get('page')
    comments = Comment.objects.filter(post__id=post_id).order_by('-created_at')
    comments = paginate_list(comments, page)
    comments_html = loader.render_to_string(
        'social/partials/comments.html',
        {'comments': comments, 'user': request.user, 'MEDIA_URL': settings.MEDIA_URL},
    )
    data['has_next'] = comments.has_next()
    data['comments_html'] = comments_html
    return JsonResponse(data)


def load_popular(request):
    page = request.POST.get('page')

    popular_posts = c.popular(request.user)
    popular_posts = paginate_list(popular_posts, page, 15)
    popular_html = loader.render_to_string(
        'social/partials/posts.html',
        {'posts': popular_posts, 'user': request.user, 'MEDIA_URL': settings.MEDIA_URL},
    )
    data['has_next'] = popular_posts.has_next()
    data['list_html'] = popular_html

    return JsonResponse(data)


def load_users(request):
    page = request.POST.get('page')

    users = c.popular_users(request.user)
    users = paginate_list(users, page, 15)
    users_html = loader.render_to_string(
        'social/partials/users.html',
        {'user': request.user, 'users': users, 'MEDIA_URL': settings.MEDIA_URL},
    )
    data['has_next'] = users.has_next()
    data['list_html'] = users_html

    return JsonResponse(data)


def load_search_results(request):
    q = request.POST.get('q')
    page = request.POST.get('page')
    results = watson.search(q)
    results = paginate_list(results, page)
    results_html = loader.render_to_string(
        'social/partials/search-results.html',
        {'results': results},
    )
    data['has_next'] = results.has_next()
    data['results_html'] = results_html
    return JsonResponse(data)


def load_notifications(request):
    page = request.POST.get('page')
    notifs = Notification.objects.filter(target_type="user", target_id=request.user.id).order_by('-created_at')
    notifs = paginate_list(notifs, page)
    notifications = []
    for n in notifs:
        notif = Notify(n)
        notification = notif.get()
        notifications.append({'message': notification, 'date': n.created_at})
        # mark unread notification as read
        if n.is_read == False:
            n.is_read = True
            n.save()

    notifs_html = loader.render_to_string(
        'social/partials/notifications.html',
        {'notifications': notifications},
    )
    data['has_next'] = notifs.has_next()
    data['notifs_html'] = notifs_html
    return JsonResponse(data)