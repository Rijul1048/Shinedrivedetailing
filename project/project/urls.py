from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from app.sitemaps import StaticSitemap
from app import views
from django.conf import settings

sitemaps = {
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('app.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

   
    path('preview-404/', views.preview_404, name='preview_404'),
]

# Custom error handlers (Django uses these when DEBUG=False)
handler404 = 'app.views.custom_404_view'