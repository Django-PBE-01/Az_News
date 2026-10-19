from django.db import models
from apps.base.models import BaseModel
from django_ckeditor_5.fields import CKEditor5Field
import os

# Create your models here.
class NewsCategory(BaseModel):
    name = models.CharField(max_length=255 , verbose_name="Category Name" , help_text="The field is saved news category")

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name


class News(BaseModel):
    title = models.CharField(max_length=255 , verbose_name="News Title" , help_text="The field is saved news title")
    description = models.TextField(verbose_name="News Description" , help_text="The field is saved news description")
    image = models.ImageField(upload_to='news_images/' , null=True, blank=True , verbose_name="News Image" , help_text="The field is saved news image")

    content = CKEditor5Field('Content', config_name='extends' )
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL , related_name='news' , verbose_name="News Category" , help_text="The field is saved news category", null=True, blank=True)
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class ContactMessage(BaseModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField(max_length=5000)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Contact message'
        verbose_name_plural = 'Contact messages'

    def __str__(self):
        return f'{self.name} — {self.email}'





def save(self, *args, **kwargs):
        print(">>> SAVE METODI ISHLADI, CATEGORY:", self.category, "TITLE:", self.title)
        
        if not self.category and self.title:
            try:
                categories = list(NewsCategory.objects.values_list('name', flat=True))
                categories_str = ", ".join(categories) if categories else "Iqtisodiyot, Siyosat, Jamiyat, Texnologiya, Sport"

                prompt = (
                    f"Quyidagi yangilik uchun ushbu kategoriyalardan eng mos bitta nomni tanlang: [{categories_str}].\n"
                    f"Faqat bitta kategoriya nomini yozing.\n\n"
                    f"Sarlavha: {self.title}\n"
                    f"Tavsif: {self.description}"
                )

                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable is not configured")

                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                ai_cat_name = response.text.strip()
                print(f"--- AI QAYTARGANI: {ai_cat_name} ---")

                cat_obj, created = NewsCategory.objects.get_or_create(name=ai_cat_name)
                self.category = cat_obj

            except Exception as e:
                print(f"!!! AI XATOLIK BERDI: {e} !!!")

        super().save(*args, **kwargs)
