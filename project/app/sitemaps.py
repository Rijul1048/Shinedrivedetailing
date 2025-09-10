from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Only index public, canonical pages
        return [
            'index',
            'about',
            'services',
            'exterior_detail',
            'interior_detail',
            'full',
            'sedan',
            'suv_5seat',
            'suv_7seat',
            'xl_suv',
        ]

    def location(self, item):
        return reverse(item)
