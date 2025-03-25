from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.tasks import update_share_statistics, clean_old_share_records, calculate_share_trends

class Command(BaseCommand):
    help = 'Update share statistics and clean old share records'

    def handle(self, *args, **options):
        start_time = timezone.now()
        self.stdout.write('Starting share statistics update...')

        # Update share statistics
        self.stdout.write('Updating share statistics...')
        update_share_statistics()
        self.stdout.write(self.style.SUCCESS('Successfully updated share statistics'))

        # Clean old records
        self.stdout.write('Cleaning old share records...')
        clean_old_share_records()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned old share records'))

        # Calculate trends
        self.stdout.write('Calculating share trends...')
        calculate_share_trends()
        self.stdout.write(self.style.SUCCESS('Successfully calculated share trends'))

        # Report completion time
        duration = timezone.now() - start_time
        self.stdout.write(self.style.SUCCESS(
            f'All tasks completed successfully in {duration.total_seconds():.2f} seconds'
        )) 