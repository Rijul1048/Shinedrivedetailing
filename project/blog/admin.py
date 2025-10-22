# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'publish_date', 'views']
    list_filter = ['status', 'category', 'tags', 'publish_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'created_date', 'updated_date']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Classification', {
            'fields': ('category', 'tags')
        }),
        ('Publication', {
            'fields': ('author', 'status', 'publish_date')
        }),
        ('Statistics', {
            'fields': ('views', 'reading_time', 'created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )