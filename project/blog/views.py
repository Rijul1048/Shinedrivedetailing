 # blog/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.utils import timezone
from .models import Post, Category, Tag
from django.shortcuts import get_object_or_404

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        ).select_related('author', 'category').prefetch_related('tags')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = "Blog - Latest Articles"
        context['meta_description'] = "Read our latest blog posts and articles on various topics."
        context['category_list'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Add SEO meta data
        context['meta_title'] = post.meta_title
        context['meta_description'] = post.meta_description
        
        # Structured data for SEO
        context['structured_data'] = self.get_structured_data(post)
        
        # Related posts
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id)[:3]
        
        return context
    
    def get_structured_data(self, post):
        return {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post.title,
            "description": post.meta_description,
            "author": {
                "@type": "Person",
                "name": post.author.get_full_name() or post.author.username
            },
            "publisher": {
                "@type": "Organization",
                "name": "Your Site Name",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://yoursite.com/static/images/logo.png"
                }
            },
            "datePublished": post.publish_date.isoformat(),
            "dateModified": post.updated_date.isoformat(),
            "image": post.featured_image.url if post.featured_image else None,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": self.request.build_absolute_uri(post.get_absolute_url())
            }
        }

# blog/views.py - Update CategoryPostListView
class CategoryPostListView(ListView):
    template_name = 'blog/post_category.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category,
            publish_date__lte=timezone.now()
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['category_list'] = Category.objects.all()  # Add this for related categories
        context['meta_title'] = self.category.meta_title or f"Posts in {self.category.name}"
        context['meta_description'] = self.category.meta_description or f"Browse all posts in {self.category.name} category"
        return context
    
class TagPostListView(ListView):
    template_name = 'blog/post_category.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            tags=self.tag,
            publish_date__lte=timezone.now()
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['meta_title'] = f"Posts tagged with {self.tag.name}"
        context['meta_description'] = f"Browse all posts tagged with {self.tag.name}"
        return context

class SearchResultsView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(status='published'),
                Q(publish_date__lte=timezone.now()),
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().select_related('author', 'category').prefetch_related('tags')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['search_query'] = query
        context['meta_title'] = f"Search Results for '{query}'"
        context['meta_description'] = f"Search results for: {query}"
        return context