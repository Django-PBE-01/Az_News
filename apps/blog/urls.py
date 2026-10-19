from django.urls import path
from .views import BlogDetailView, BlogListView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('<int:blog_id>/', BlogDetailView.as_view(), name='detail'),
]
