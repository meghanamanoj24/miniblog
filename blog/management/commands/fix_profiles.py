from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Profile

class Command(BaseCommand):
    help = 'Creates missing user profiles'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created = 0
        for user in users:
            profile, was_created = Profile.objects.get_or_create(user=user)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        
        if created == 0:
            self.stdout.write(self.style.SUCCESS('All users already have profiles'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {created} new profiles')) 