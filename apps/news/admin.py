import os
import logging
import re

from django.contrib import admin
from google import genai
from google.genai import types

from apps.news.models import ContactMessage, News, NewsCategory

logger = logging.getLogger(__name__)


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        if not obj.category and obj.title:
            categories = list(NewsCategory.objects.values_list('name', flat=True))
            if categories:
                try:
                    api_key = os.getenv('GEMINI_API_KEY')
                    if api_key:
                        client = genai.Client(
                            api_key=api_key,
                            http_options=types.HttpOptions(timeout=1000000),
                        )
                        response = client.models.generate_content(
                            model='gemini-3.5-flash-lite',
                            contents=(
                                'Tanlovdan yangilikka mos bitta kategoriya nomini qaytar. '
                                'Faqat nomni yoz. Kategoriyalar: '
                                f'{", ".join(categories)}. Sarlavha: {obj.title[:255]}'
                            ),
                            config=types.GenerateContentConfig(
                                max_output_tokens=20,
                                temperature=0,
                            ),
                        )
                        answer = (response.text or '').strip()
                        normalize = lambda value: re.sub(r'[^\w]+', '', value.casefold())
                        normalized_answer = normalize(answer)
                        matched_name = next(
                            (name for name in categories if normalize(name) == normalized_answer),
                            None,
                        )
                        if matched_name:
                            obj.category = NewsCategory.objects.get(name=matched_name)
                        else:
                            logger.warning('Gemini returned an unknown news category: %r', answer)
                except Exception:
                    # Keep news saving even when AI is unavailable, but log the cause for diagnosis.
                    logger.exception('Gemini could not assign a news category')

        super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_active')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
