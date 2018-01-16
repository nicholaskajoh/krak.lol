from django.core.management.base import BaseCommand, CommandError
from social.models import Profile

# modify the urls of registered users to include "@" char
class Command(BaseCommand):
  help = 'Modifies urls of registered users to include "@" character'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    users_changed = 0
    # loop thru' all users and modify their urls
    profiles = Profile.objects.all();
    for profile in profiles:
      if not '@' in profile.url:
        profile.url = '/@' + profile.user.username + '/'
        profile.save()
        users_changed += 1

    self.stdout.write(self.style.SUCCESS('Mod complete! %i users changed.' % users_changed))