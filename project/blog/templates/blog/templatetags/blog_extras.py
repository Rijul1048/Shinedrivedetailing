# blog/templatetags/blog_extras.py
from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """Replace or add a parameter in the URL"""
    dict_ = request.GET.copy()
    dict_[field] = value
    return urlencode(dict_)