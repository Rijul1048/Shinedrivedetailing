# blog/templatetags/blog_extras.py
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
import json

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """Replace or add a parameter in the URL"""
    dict_ = request.GET.copy()
    dict_[field] = value
    return urlencode(dict_)

@register.simple_tag
def blog_meta_title(post=None, category=None, tag=None, search_query=None):
    """Generate SEO-optimized meta titles for blog pages"""
    if post:
        return f"{post.meta_title} | ShineDrive Detailing - Waterloo, Kitchener, Cambridge"
    elif category:
        return f"{category.meta_title or category.name} | Car Detailing Tips | ShineDrive Detailing - Waterloo, Kitchener, Cambridge"
    elif tag:
        return f"Posts tagged '{tag.name}' | Car Detailing Blog | ShineDrive Detailing - Waterloo, Kitchener, Cambridge"
    elif search_query:
        return f"Search Results for '{search_query}' | ShineDrive Detailing Blog - Waterloo, Kitchener, Cambridge"
    else:
        return "Car Detailing Tips & Blog | ShineDrive Detailing - Waterloo, Kitchener, Cambridge, Elmira"

@register.simple_tag
def blog_meta_description(post=None, category=None, tag=None, search_query=None):
    """Generate SEO-optimized meta descriptions for blog pages"""
    if post:
        return post.meta_description or f"Read our expert guide on {post.title.lower()}. Professional car detailing tips from ShineDrive Detailing serving Waterloo, Kitchener, Cambridge, and Elmira, Ontario."
    elif category:
        return category.meta_description or f"Expert {category.name.lower()} tips and guides from ShineDrive Detailing. Professional car care advice for Waterloo, Kitchener, Cambridge, and Elmira, Ontario residents."
    elif tag:
        return f"Discover professional car detailing tips and guides tagged with '{tag.name}' from ShineDrive Detailing experts. Serving Waterloo, Kitchener, Cambridge, and Elmira, Ontario."
    elif search_query:
        return f"Search results for '{search_query}' in our car detailing blog. Find expert tips and professional advice from ShineDrive Detailing serving Waterloo, Kitchener, Cambridge, and Elmira, Ontario."
    else:
        return "Expert car detailing tips, guides, and professional advice from ShineDrive Detailing. Serving Waterloo, Kitchener, Cambridge, Elmira, Woolwich, and St. Jacobs, Ontario. Learn how to maintain your vehicle's appearance with our comprehensive blog."

@register.simple_tag
def blog_keywords(post=None, category=None, tag=None):
    """Generate SEO keywords for blog pages"""
    base_keywords = [
        "car detailing Waterloo", "car detailing Kitchener", "car detailing Cambridge",
        "car detailing Elmira Ontario", "car detailing near me", "auto detailing Waterloo",
        "auto detailing Kitchener", "auto detailing Cambridge", "vehicle care Waterloo",
        "professional detailing Waterloo", "car cleaning Kitchener", "auto care Cambridge",
        "ShineDrive Detailing", "car detailing Woolwich", "car detailing St Jacobs",
        "mobile car detailing Waterloo", "car detailing services Kitchener"
    ]
    
    if post and post.tags.exists():
        tag_keywords = [tag.name for tag in post.tags.all()]
        return ", ".join(base_keywords + tag_keywords)
    elif category:
        category_keywords = [category.name.lower(), f"{category.name.lower()} tips", f"{category.name.lower()} guide"]
        return ", ".join(base_keywords + category_keywords)
    elif tag:
        tag_keywords = [tag.name, f"{tag.name} tips", f"{tag.name} guide", f"car {tag.name}"]
        return ", ".join(base_keywords + tag_keywords)
    else:
        return ", ".join(base_keywords)

@register.simple_tag
def blog_structured_data(post=None, category=None, tag=None):
    """Generate JSON-LD structured data for blog pages"""
    if post:
        structured_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post.title,
            "description": post.meta_description or post.excerpt,
            "author": {
                "@type": "Person",
                "name": post.author.get_full_name() or post.author.username,
                "url": "https://shinedrivedetailing.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "ShineDrive Detailing",
                "url": "https://shinedrivedetailing.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://shinedrivedetailing.com/static/images/logo.png"
                },
                "address": {
                    "@type": "PostalAddress",
                    "addressCountry": "CA",
                    "addressRegion": "Ontario",
                    "addressLocality": "Waterloo"
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+1-548-398-7555",
                    "contactType": "customer service",
                    "email": "shinedrive2024@gmail.com",
                    "availableLanguage": "English",
                    "hoursAvailable": {
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                        "opens": "07:00",
                        "closes": "19:00"
                    }
                },
                "areaServed": [
                    {"@type": "City", "name": "Waterloo, ON"},
                    {"@type": "City", "name": "Kitchener, ON"},
                    {"@type": "City", "name": "Cambridge, ON"},
                    {"@type": "City", "name": "Elmira, ON"},
                    {"@type": "City", "name": "Woolwich, ON"},
                    {"@type": "City", "name": "St. Jacobs, ON"}
                ]
            },
            "datePublished": post.publish_date.isoformat(),
            "dateModified": post.updated_date.isoformat(),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://shinedrivedetailing.com{post.get_absolute_url()}"
            },
            "articleSection": post.category.name if post.category else "Car Detailing",
            "keywords": [tag.name for tag in post.tags.all()] if post.tags.exists() else ["car detailing"],
            "wordCount": len(post.content.split()) if post.content else 0
        }
        
        if post.featured_image:
            structured_data["image"] = {
                "@type": "ImageObject",
                "url": f"https://shinedrivedetailing.com{post.featured_image.url}",
                "width": 800,
                "height": 600
            }
        
        return mark_safe(json.dumps(structured_data, indent=2))
    
    elif category:
        structured_data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": f"{category.name} - Car Detailing Tips",
            "description": category.meta_description or f"Expert {category.name.lower()} tips and guides from ShineDrive Detailing",
            "url": f"https://shinedrivedetailing.com/blog/category/{category.slug}/",
            "mainEntity": {
                "@type": "ItemList",
                "name": f"{category.name} Articles",
                "description": f"Collection of {category.name.lower()} articles and guides"
            },
            "publisher": {
                "@type": "Organization",
                "name": "ShineDrive Detailing",
                "url": "https://shinedrivedetailing.com"
            }
        }
        return mark_safe(json.dumps(structured_data, indent=2))
    
    else:
        # Blog homepage structured data
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "ShineDrive Detailing Blog",
            "description": "Expert car detailing tips, guides, and professional advice",
            "url": "https://shinedrivedetailing.com/blog/",
            "publisher": {
                "@type": "Organization",
                "name": "ShineDrive Detailing",
                "url": "https://shinedrivedetailing.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://shinedrivedetailing.com/static/images/logo.png"
                }
            }
        }
        return mark_safe(json.dumps(structured_data, indent=2))

@register.simple_tag
def blog_canonical_url(request, post=None, category=None, tag=None):
    """Generate canonical URLs for blog pages"""
    base_url = "https://shinedrivedetailing.com"
    
    if post:
        return f"{base_url}{post.get_absolute_url()}"
    elif category:
        return f"{base_url}/blog/category/{category.slug}/"
    elif tag:
        return f"{base_url}/blog/tag/{tag.slug}/"
    else:
        return f"{base_url}{request.path}"

@register.simple_tag
def blog_faq_structured_data():
    """Generate FAQ structured data for car detailing blog"""
    faq_data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Do you provide car detailing services in Waterloo, Kitchener, and Cambridge?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes! ShineDrive Detailing proudly serves Waterloo, Kitchener, Cambridge, Elmira, Woolwich, and St. Jacobs, Ontario. We offer both mobile detailing services where we come to you, and you can also visit our location. Contact us at +1-548-398-7555 to book your service."
                }
            },
            {
                "@type": "Question",
                "name": "What is professional car detailing?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Professional car detailing is a comprehensive cleaning and restoration process that goes beyond a regular car wash. It includes thorough cleaning of both interior and exterior surfaces, paint correction, protection treatments, and attention to every detail to restore your vehicle to its best possible condition."
                }
            },
            {
                "@type": "Question",
                "name": "How often should I get my car detailed?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The frequency of car detailing depends on your usage and environment. For daily drivers in Waterloo, Kitchener, and Cambridge areas, we recommend professional detailing every 3-4 months. High-end vehicles or those in harsh Ontario weather conditions may need more frequent service."
                }
            },
            {
                "@type": "Question",
                "name": "Do you offer mobile car detailing in Elmira, Woolwich, and St. Jacobs?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes! We provide convenient mobile detailing services throughout our service area including Elmira, Woolwich, and St. Jacobs, Ontario. Our professionals come to your location with all necessary equipment and supplies. We're available 7 days a week from 7am to 7pm."
                }
            },
            {
                "@type": "Question",
                "name": "What's the difference between car wash and car detailing?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "A car wash focuses on basic cleaning of exterior surfaces, while car detailing is a comprehensive process that includes deep cleaning, paint correction, interior deep cleaning, protection treatments, and attention to every detail. Detailing provides longer-lasting results and better protection for your vehicle."
                }
            },
            {
                "@type": "Question",
                "name": "Can detailing remove scratches from my car?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Professional detailing can significantly improve or remove light scratches through paint correction techniques. However, deep scratches that penetrate the clear coat may require more extensive repair. Our experts can assess your vehicle and recommend the best approach for scratch removal and paint restoration."
                }
            },
            {
                "@type": "Question",
                "name": "How long does a full car detailing service take?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The duration depends on the service package and vehicle condition. A basic detail typically takes 2-3 hours, while a comprehensive full detail can take 4-6 hours. Premium packages with paint correction may require a full day. We provide accurate time estimates when you book your service."
                }
            },
            {
                "@type": "Question",
                "name": "What are your business hours?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "ShineDrive Detailing is open 7 days a week from 7:00 AM to 7:00 PM. We serve Waterloo, Kitchener, Cambridge, Elmira, Woolwich, and St. Jacobs, Ontario. You can reach us at +1-548-398-7555 or email us at shinedrive2024@gmail.com to schedule your appointment."
                }
            }
        ]
    }
    return mark_safe(json.dumps(faq_data, indent=2))
