from django.contrib import admin
from apps.accunts.models import CostumeUser
# Register your models here.

@admin.register(CostumeUser)
class CostumeUserAdmin(admin.ModelAdmin):
    list_display = ('email',  'is_active')
    search_fields = ('email',)
    ordering = ('id',)


