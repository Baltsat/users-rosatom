from django.contrib import admin

from .models import QAItem


# Register your models here.

class QAItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'sentiment', 'j', 'cluster_id', 'list_display_links',)
    search_fields = ('question', 'cluster_id',)
    list_display_links = ('question',)

admin.site.register(QAItem, QAItemAdmin)