from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", default="fas fa-globe")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Location(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = RichTextField()
    featured_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travel_duration = models.PositiveIntegerField(help_text="Duration in days", null=True, blank=True)
    travel_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Cost in USD")
    travel_tips = models.TextField(blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging')
    ], blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    @property
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'Reply by {self.author.username} on {self.comment.content[:30]}'
