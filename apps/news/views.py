from django.shortcuts import render
from django.views.generic import TemplateView
from apps.news.models import News,NewsCategory
from apps.news.models import ContactMessage
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = NewsCategory.objects.filter(is_active=True)
        active_news = News.objects.filter(is_active=True).select_related('category').order_by('-created_at')
        top_news = active_news.first()
        other_news = active_news.exclude(pk=top_news.pk) if top_news else active_news.none()
        news1 = other_news[:3]
        news2 = other_news[3:8]
        category_id=self.request.GET.get('category')
        if category_id:
            news_filtered = active_news.filter(category=category_id, is_active=True)
            context['news_filtered'] = news_filtered


        context.update({
            'categories': categories,
            'top_news': top_news,
            'news1': news1,
            'news2': news2,
            'user': user,
            })
        return context


class NewsDetailView(TemplateView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('news_id')
        news = News.objects.filter(pk=news_id, is_active=True).select_related('category').first()
        context['news'] = news
        return context


class NewsListView(ListView):
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = News.objects.filter(is_active=True).select_related('category').order_by('-created_at')
        category_id = self.kwargs.get('category_id') or self.request.GET.get('category')
        if category_id and str(category_id).isdigit():
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['selected_category'] = str(self.kwargs.get('category_id') or self.request.GET.get('category', ''))
        return context


class NewsSearchView(ListView):
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return News.objects.none()
        return News.objects.filter(is_active=True).filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(content__icontains=query)
            | Q(category__name__icontains=query)
        ).select_related('category').order_by('-created_at').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['search_query'] = self.request.GET.get('q', '').strip()
        context['is_search'] = True
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect

        required = ('name', 'email', 'message')
        values = {field: request.POST.get(field, '').strip() for field in required}
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(values['email'])
            valid = all(values.values())
        except ValidationError:
            valid = False
        if valid:
            ContactMessage.objects.create(**values)
            messages.success(request, 'Xabaringiz qabul qilindi. Tez orada siz bilan bog‘lanamiz.')
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni to‘ldiring.')
        return redirect('news:contact')
    
