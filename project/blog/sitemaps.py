# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category, Tag

class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return obj.get_absolute_url()

class BlogCategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog:category_posts', kwargs={'slug': obj.slug})

class BlogTagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse('blog:tag_posts', kwargs={'slug': obj.slug})

class BlogStaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return ['blog:post_list', 'blog:search']

    def location(self, item):
        return reverse(item)
