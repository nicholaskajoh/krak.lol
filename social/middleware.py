from django.contrib.auth.models import User
from social.models import Profile
from django.utils.timezone import now

class SetLastSeenMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            # update user last seen time after request has been processed
            Profile.objects.filter(user=request.user).update(last_seen=now())
        return None