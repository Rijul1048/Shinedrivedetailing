# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.PostDetailView.as_view(), name='post_detail'),
]