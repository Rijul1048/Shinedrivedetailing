# views.py
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from .utils.email import send_booking_confirmation, send_booking_notification
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def index(request):
    context = {
        'active_page': 'index',
        'title': 'ShineDrive Detailing - Premium Car Detailing Services',
        'meta_description': 'Professional car detailing, washing, and ceramic coating services in your area. Get your car looking brand new with ShineDrive Detailing.'
    }
    return render(request, "index.html", context)

def sedan(request):
    context = {
        'active_page': 'booking',
        'title': 'Sedan/Coupe Detailing - ShineDrive Detailing',
        'meta_description': 'Book premium full, interior, or exterior detailing services for your Sedan or Coupe with ShineDrive Detailing.'
    }
    return render(request, "sedan.html", context)

def suv_5seat(request):
    context = {
        'active_page': 'booking',
        'title': '5-Seat SUV Detailing - ShineDrive Detailing',
        'meta_description': 'Book professional full, interior, or exterior car detailing for your 5-seat SUV at ShineDrive Detailing.'
    }
    return render(request, "suv_5seat.html", context)

def suv_7seat(request):
    context = {
        'active_page': 'booking',
        'title': 'Pick Up/7-Seat SUV Detailing - ShineDrive Detailing',
        'meta_description': 'Specialized car detailing services for Pick Up trucks and 7-seat SUVs. Choose from full, interior, or exterior packages.'
    }
    return render(request, "suv_7seat.html", context)

def xl_suv(request):
    context = {
        'active_page': 'booking',
        'title': 'XL SUV Detailing - ShineDrive Detailing',
        'meta_description': 'Comprehensive car detailing for XL SUVs. Explore our full, interior, and exterior detailing packages.'
    }
    return render(request, "xl_suv.html", context)

def aboutus(request):
    context = {
        'active_page': 'aboutus',
        'title': 'About Us - ShineDrive Detailing',
        'meta_description': 'Learn more about ShineDrive Detailing, our mission, and our commitment to providing the best car detailing experience.'
    }
    return render(request, "aboutus.html", context)

def services_view(request):
    context = {
        'active_page': 'services',
        'title': 'Our Services - ShineDrive Detailing',
        'meta_description': 'Discover our range of premium car detailing services, including full detail, interior cleaning, exterior wash, and ceramic coating.'
    }
    return render(request, "services.html", context)

def exterior_detail_view(request):
    context = {
        'active_page': 'exterior_detail',
        'title': 'Exterior Car Detailing - ShineDrive Detailing',
        'meta_description': 'Restore your car\'s exterior shine with our professional detailing services, including washing, waxing, and paint correction.'
    }
    return render(request, "detailing/exterior_detail.html", context)

def interior_detail_view(request):
    context = {
        'active_page': 'interior_detail',
        'title': 'Interior Car Detailing - ShineDrive Detailing',
        'meta_description': 'Deep clean and sanitize your car\'s interior with our expert detailing services. Upholstery cleaning, vacuuming, and odor removal.'
    }
    return render(request, "detailing/interior_detail.html", context)

def full(request):
    context = {
        'active_page': 'services',
        'title': 'Full Car Detailing - ShineDrive Detailing',
        'meta_description': 'Get the complete car detailing experience with our full package, covering both interior and exterior cleaning and protection.'
    }
    return render(request, "detailing/full_detail.html", context)

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save()
                
                # Send confirmation email to customer
                if booking.email:
                    send_booking_confirmation(booking)
                
                # Send notification email to yourself (business owner)
                send_booking_notification(booking)
                
                messages.success(request, 'Booking created successfully!')
                return redirect('booking_thank_you', slug=booking.slug)
            except Exception as e:
                # Add more specific error handling
                messages.error(request, f'Error creating booking: {str(e)}')
        # If form is not valid, it will fall through and render the template with errors
    else:
        initial = {
            'vehicle_type': request.GET.get('vehicle', 'sedan'),
            'service_type': request.GET.get('service', 'full'),
            'package_type': request.GET.get('package', 'gold'),
        }
        form = BookingForm(initial=initial)
    
    context = {
        'form': form,
        'active_page': 'booking',
        'title': 'Book Your Car Detailing Appointment - ShineDrive Detailing',
        'meta_description': 'Schedule your next car detailing appointment online. Choose your vehicle type, service, and package for a perfect shine.'
    }
    return render(request, 'booking/custom_booking.html', context)


def booking_thank_you(request, slug):
    try: 
        booking = get_object_or_404(Booking, slug=slug)
        context = {
            'booking': booking,
            'active_page': 'thank_you',
            'title': f'Booking Confirmed - {booking.full_name} - ShineDrive Detailing',
            'meta_description': f'Your car detailing appointment for {booking.vehicle_type} {booking.service_type} on {booking.date} is confirmed. Details of your booking.'
        }
        return render(request, 'booking/thanku.html', context)
    except Exception as e:
        messages.error(request, 'Booking not found.')
        # Log the error here
        return redirect('index')

def custom_404_view(request, exception=None):
    response = render(request, '404.html', status=404)
    return response

def preview_404(request):
    # Helpful while DEBUG=True to see the 404 page without forcing an actual 404
    return HttpResponseNotFound(render(request, '404.html').content)
    
@csrf_exempt
@require_POST
def send_booking_email(request):
    try:
        data = json.loads(request.body)
        
        # Extract form data
        vehicle_type = data.get('vehicle_type', '')
        service_type = data.get('service_type', '')
        package_type = data.get('package_type', '')
        package_price = data.get('package_price', '')
        full_name = data.get('full_name', '')
        mobile = data.get('mobile', '')
        email = data.get('email', '')
        date = data.get('date', '')
        special_requests = data.get('special_requests', '')
        
        # Create email content
        subject = f"New Car Detailing Booking - {full_name}"
        
        message = f"""
        New Booking Details:
        
        Customer Information:
        - Name: {full_name}
        - Mobile: {mobile}
        - Email: {email}
        
        Service Details:
        - Vehicle Type: {vehicle_type}
        - Service Type: {service_type}
        - Package: {package_type}
        - Price: ${package_price} CAD
        - Date: {date}
        
        Special Requests:
        {special_requests}
        
        This booking was made through your website.
        """
        
        # Send email
        send_mail(
            subject,
            message,    
            settings.DEFAULT_FROM_EMAIL,  # From email
            [settings.BUSINESS_EMAIL],   # Use your business email from settings
            fail_silently=False,
        )
        
        return JsonResponse({'status': 'success', 'message': 'Booking confirmed and email sent!'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /booking/thank-you/",
        f"Sitemap: {request.build_absolute_uri(reverse('django.contrib.sitemaps.views.sitemap'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")