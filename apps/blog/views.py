from django.views.generic import DetailView, ListView
from .models import Blog, BlogCategory


class BlogListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'blog_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = Blog.objects.filter(is_active=True).prefetch_related('category').order_by('-created_at')
        category = self.request.GET.get('category')
        if category and category.isdigit():
            queryset = queryset.filter(category__id=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_id'

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).prefetch_related('category')
