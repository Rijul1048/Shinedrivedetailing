from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from app.sitemaps import StaticSitemap
from blog.sitemaps import BlogPostSitemap, BlogCategorySitemap, BlogTagSitemap, BlogStaticSitemap
from app import views

sitemaps = {
    'static': StaticSitemap,
    'blog_posts': BlogPostSitemap,
    'blog_categories': BlogCategorySitemap,
    'blog_tags': BlogTagSitemap,
    'blog_static': BlogStaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('app.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

   
    path('preview-404/', views.preview_404, name='preview_404'),
]

# Serve robots.txt from static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers (Django uses these when DEBUG=False)
handler404 = 'app.views.custom_404_view'