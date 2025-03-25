from django.contrib import admin
from .models import Category, Location, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'location', 'created_date', 'travel_date', 'difficulty_level')
    list_filter = ('category', 'created_date', 'difficulty_level', 'location__country')
    search_fields = ('title', 'content', 'location__name', 'location__country')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    raw_id_fields = ('author',)
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'content', 'featured_image')
        }),
        ('Categories and Location', {
            'fields': ('category', 'location')
        }),
        ('Travel Details', {
            'fields': ('travel_date', 'travel_duration', 'travel_cost', 'difficulty_level')
        }),
        ('Additional Information', {
            'fields': ('travel_tips', 'best_time_to_visit')
        }),
        ('Metadata', {
            'fields': ('created_date', 'updated_date', 'likes')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date', 'rating')
    list_filter = ('created_date', 'rating')
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('author', 'post')
