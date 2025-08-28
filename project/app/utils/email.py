# app/utils/email.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_booking_confirmation(booking):
    """
    Send booking confirmation email to the customer
    """
    subject = f"Booking Confirmation - Shine Car Detailing"
    
    # Format the date properly
    booking_date = booking.date.strftime('%B %d, %Y') if booking.date else "Not specified"
    
    # Get display values for choices
    vehicle_type_display = booking.get_vehicle_type_display()
    service_type_display = booking.get_service_type_display()
    package_type_display = booking.get_package_type_display()
    
    # Create email content
    context = {
        'booking': booking,
        'vehicle_type_display': vehicle_type_display,
        'service_type_display': service_type_display,
        'package_type_display': package_type_display,
        'booking_date': booking_date,
    }
    
    # Render HTML template
    html_message = render_to_string('emails/booking_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email to customer
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_booking_notification(booking):
    """
    Send booking notification email to the business owner
    """
    subject = f"New Car Detailing Booking - {booking.full_name}"
    
    # Format the date properly
    booking_date = booking.date.strftime('%B %d, %Y') if booking.date else "Not specified"
    
    # Get display values for choices
    vehicle_type_display = booking.get_vehicle_type_display()
    service_type_display = booking.get_service_type_display()
    package_type_display = booking.get_package_type_display()
    
    message = f"""
New Booking Details:

Customer Information:
- Name: {booking.full_name}
- Mobile: {booking.mobile}
- Email: {booking.email or 'Not provided'}

Service Details:
- Vehicle Type: {vehicle_type_display}
- Service Type: {service_type_display}
- Package: {package_type_display}
- Date: {booking_date}

Special Requests:
{booking.special_requests or 'None'}

This booking was made through your website.
"""
    
    # Send email to your business email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.BUSINESS_EMAIL],  # Use your business email from settings
        fail_silently=False,
    )