from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Booking

# Register your models here.
class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'mobile', 'vehicle_type', 'service_type', 'package_type', 'date', 'time', 'created_at')
    list_filter = ('vehicle_type', 'service_type', 'package_type', 'date')
    search_fields = ('full_name', 'email', 'mobile')
    date_hierarchy = 'date'

admin.site.register(Booking, BookingAdmin)
