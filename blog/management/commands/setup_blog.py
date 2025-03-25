from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from blog.models import Category, Post, Profile
import os

class Command(BaseCommand):
    help = 'Setup and verify blog configuration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting blog setup...')
        
        # 1. Check and create necessary directories
        directories = ['static', 'media', 'logs', 'templates/blog/emails']
        for directory in directories:
            path = os.path.join(settings.BASE_DIR, directory)
            if not os.path.exists(path):
                os.makedirs(path)
                self.stdout.write(self.style.SUCCESS(f'Created directory: {directory}'))
            else:
                self.stdout.write(f'Directory exists: {directory}')

        # 2. Setup default site
        site, created = Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'localhost:8000',
                'name': settings.SITE_NAME
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created default site configuration'))
        else:
            self.stdout.write('Site configuration exists')

        # 3. Create default categories
        default_categories = ['Travel Tips', 'Destinations', 'Food & Culture', 'Adventure']
        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)
        self.stdout.write(self.style.SUCCESS('Created default categories'))

        # 4. Verify superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('No superuser found! Please create one using:'))
            self.stdout.write('python manage.py createsuperuser')

        # 5. Verify profiles for existing users
        users_without_profiles = User.objects.filter(profile__isnull=True)
        if users_without_profiles.exists():
            for user in users_without_profiles:
                Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profiles for {users_without_profiles.count()} users'))

        # 6. Final verification
        self.stdout.write('\nVerification Summary:')
        self.stdout.write(f'- Categories: {Category.objects.count()}')
        self.stdout.write(f'- Users: {User.objects.count()}')
        self.stdout.write(f'- Posts: {Post.objects.count()}')
        self.stdout.write(f'- Profiles: {Profile.objects.count()}')

        self.stdout.write(self.style.SUCCESS('\nSetup completed successfully!')) 