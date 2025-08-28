

from django.db import models
import uuid

class Booking(models.Model):
    VEHICLE_CHOICES = [
        ('sedan', 'Sedan/Coupe (2 Seats)'),
        ('suv5', 'SUV (5 Seats)'),
        ('suv7', 'Pick Up/7-Seat SUV'),
        ('xlsuv', 'XL SUV')
    ]
    
    SERVICE_CHOICES = [
        ('full', 'Full Detail'),
        ('interior', 'Interior Detail'),
        ('exterior', 'Exterior Detail')
    ]
    
    PACKAGE_CHOICES = [
        ('bronze', 'Bronze'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum')
    ]
    
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    package_type = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_vehicle_type_display()} - {self.date}"