from django.db import models
from apps.base.models import BaseModel
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class BlogCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Category Name", help_text="The field is saved blog category")

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class Blog(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Blog Title", help_text="The field is saved blog title")
    description = models.TextField(verbose_name="Blog Description", help_text="The field is saved blog description")
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name="Blog Image", help_text="The field is saved blog image")
    category = models.ManyToManyField(BlogCategory, verbose_name="Blog Category", help_text="The field is saved blog category")
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

