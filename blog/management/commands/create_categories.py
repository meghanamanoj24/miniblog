from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for the travel blog'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Destinations',
                'description': 'Explore different travel destinations around the world'
            },
            {
                'name': 'Travel Tips',
                'description': 'Essential tips and advice for travelers'
            },
            {
                'name': 'Adventure Travel',
                'description': 'Thrilling adventures and outdoor activities'
            },
            {
                'name': 'Food & Cuisine',
                'description': 'Local food experiences and culinary adventures'
            },
            {
                'name': 'Culture & Heritage',
                'description': 'Cultural experiences and historical sites'
            },
            {
                'name': 'Budget Travel',
                'description': 'Tips for traveling on a budget'
            },
            {
                'name': 'Luxury Travel',
                'description': 'Luxury travel experiences and accommodations'
            },
            {
                'name': 'Solo Travel',
                'description': 'Tips and experiences for solo travelers'
            },
            {
                'name': 'Family Travel',
                'description': 'Family-friendly destinations and activities'
            },
            {
                'name': 'Road Trips',
                'description': 'Road trip experiences and itineraries'
            },
            {
                'name': 'Beach & Island',
                'description': 'Beach destinations and island getaways'
            },
            {
                'name': 'Mountain & Trekking',
                'description': 'Mountain destinations and trekking experiences'
            },
            {
                'name': 'City Breaks',
                'description': 'Urban travel experiences and city guides'
            },
            {
                'name': 'Photography',
                'description': 'Travel photography tips and inspiration'
            },
            {
                'name': 'Travel Gear',
                'description': 'Reviews and recommendations for travel gear'
            }
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created category "{category.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists')) 