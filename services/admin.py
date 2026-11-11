from django.contrib import admin

# Register your models here.

from .models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'short_code',
        'clicks',
        'created_at'
    )

    search_fields = (
        'title',
        'original_url',
        'user__username'
    )

    list_filter = ('created_at',)
    readonly_fields = ('short_code', 'clicks', 'created_at')
