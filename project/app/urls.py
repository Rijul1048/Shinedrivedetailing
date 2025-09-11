from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.aboutus, name='about'),
    
    # Service pages
    path('services/', views.services_view, name='services'),
    path('detailing/exterior_detail/', views.exterior_detail_view, name='exterior_detail'),
    path('detailing/interior_detail/', views.interior_detail_view, name='interior_detail'),
    path('detailing/full_detail/', views.full, name='full'),
    
    # Vehicle pages
    path('sedan/', views.sedan, name='sedan'),
    path('suv_5seat/', views.suv_5seat, name='suv_5seat'),
    path('suv_7seat/', views.suv_7seat, name='suv_7seat'),
    path('xl_suv/', views.xl_suv, name='xl_suv'),
    
    # Booking system
    path('booking/', views.booking_view, name='booking'),
    path('booking/thank-you/<slug:slug>/', views.booking_thank_you, name='booking_thank_you'),
    
    # Email endpoint (for AJAX requests if needed)
    path('send-booking-email/', views.send_booking_email, name='send_booking_email'),

    # robots.txt
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # Legal pages
    path('privacy-policy/', views.privacy_policy, name='privacy'),
    path('terms-and-conditions/', views.terms_conditions, name='terms'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)