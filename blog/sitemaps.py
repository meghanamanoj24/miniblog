from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category, Tag

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_date or obj.created_date

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog:category-detail', args=[obj.slug])

class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse('blog:tagged', args=[obj.slug])

class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['blog:post-list', 'blog:category-list', 'blog:tag-list']

    def location(self, item):
        return reverse(item) 