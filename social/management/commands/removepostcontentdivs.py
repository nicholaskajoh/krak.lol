from django.core.management.base import BaseCommand, CommandError
from social.models import Post
import re

# remove wrapping divs from post content fields
class Command(BaseCommand):
  help = 'Removes wrapping divs from post content fields'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    affected_posts = 0
    # loop thru' all posts and modify their content
    posts = Post.objects.all();
    for post in posts:
      post.content = re.sub(r'<(div|\/div)>', '', post.content, flags=re.IGNORECASE)
      post.save()
      affected_posts += 1

    self.stdout.write(self.style.SUCCESS('Mod complete! %i posts affected.' % affected_posts))