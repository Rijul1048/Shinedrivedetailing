from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime

class StaticSitemap(Sitemap):
    protocol = 'https'
    
    def items(self):

        return [
            'index',           
            'services',        
            'full',           
            'exterior_detail', 
            'interior_detail',   
            'sedan',          
            'suv_5seat',      
            'suv_7seat',      
            'xl_suv',         
            'about',          
            'privacy',        
            'terms',          
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):

        priorities = {
            'index': 1.0,           
            'services': 0.9,        
            'full': 0.9,           
            'exterior_detail': 0.8, 
            'interior_detail': 0.8, 
            'sedan': 0.7,          
            'suv_5seat': 0.7,        
            'suv_7seat': 0.7,      
            'xl_suv': 0.7,         
            'about': 0.6,          
            'privacy': 0.3,        
            'terms': 0.3,          
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        change_frequencies = {
            'index': 'weekly',      
            'services': 'monthly',  
            'full': 'monthly',     
            'exterior_detail': 'monthly',
            'interior_detail': 'monthly',
            'sedan': 'yearly',     
            'suv_5seat': 'yearly',
            'suv_7seat': 'yearly', 
            'xl_suv': 'yearly',
            'about': 'yearly',     
            'privacy': 'yearly',   
            'terms': 'yearly',     
        }
        return change_frequencies.get(item, 'weekly')

    def lastmod(self, item):

        base_dates = {
            'index': datetime(2025, 9, 30),
            'services': datetime(2025, 9, 30),
            'full': datetime(2025, 9, 30),
            'exterior_detail': datetime(2025, 9, 30),
            'interior_detail': datetime(2025, 9, 30),
            'sedan': datetime(2025, 9, 30),
            'suv_5seat': datetime(2025, 9, 30),
            'suv_7seat': datetime(2025, 9, 30),
            'xl_suv': datetime(2025, 9, 30),
            'about': datetime(2025, 9, 30),
            'privacy': datetime(2025, 9, 30),
            'terms': datetime(2025, 9, 30),
        }
        return base_dates.get(item, datetime.now())