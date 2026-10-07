from django.contrib import admin
from apps.blog.models import BlogCategory , Blog

# Register your models here.
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'created_at', 'updated_at', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('id',)
