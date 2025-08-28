from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Booking

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'services', 'exterior_detail', 'interior_detail', 'full', 'sedan', 'suv_5seat', 'suv_7seat', 'xl_suv']

    def location(self, item):
        return reverse(item)

class BookingSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Booking.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('booking_thank_you', kwargs={'slug': obj.slug})
