from django.urls import path
from apps.news.views import AboutView, ContactView, HomeView, NewsDetailView, NewsListView, NewsSearchView

app_name = 'news'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('yangiliklar/', NewsListView.as_view(), name='latest'),
    path('qidiruv/', NewsSearchView.as_view(), name='search'),
    path('kategoriya/<int:category_id>/', NewsListView.as_view(), name='category'),
    path('biz-haqimizda/', AboutView.as_view(), name='about'),
    path('boglanish/', ContactView.as_view(), name='contact'),
    path('news/<int:news_id>/', NewsDetailView.as_view(), name='details'),
] 
