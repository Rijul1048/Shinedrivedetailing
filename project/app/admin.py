from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Booking

class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'mobile', 'vehicle_type', 'service_type', 'package_type', 'date', 'time', 'created_at', 'custom_actions')
    list_filter = ('vehicle_type', 'service_type', 'package_type', 'date')
    search_fields = ('full_name', 'email', 'mobile')
    date_hierarchy = 'date'
    
    def custom_actions(self, obj):
        return format_html(
            '<a class="button" href="{}" style="background: #dc3545; color: white; padding: 4px 8px; text-decoration: none; border-radius: 3px; font-size: 12px; margin-right: 5px;">Delete</a>'
            '<a class="button" href="{}" style="background: #007bff; color: white; padding: 4px 8px; text-decoration: none; border-radius: 3px; font-size: 12px;">Edit</a>',
            reverse('admin:app_booking_delete', args=[obj.pk]),
            reverse('admin:app_booking_change', args=[obj.pk])
        )
    custom_actions.short_description = 'Actions'

admin.site.register(Booking, BookingAdmin)