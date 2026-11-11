from django.db import models
from django.contrib.auth.models import User
import secrets
from urllib.parse import urlparse

# Create your models here.

class ShortLink(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='short_links'
    )

    title = models.CharField(max_length=100)
    original_url = models.URLField(max_length=2000)

    short_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True
    )

    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def favicon_url(self):
        domain = urlparse(self.original_url).hostname

        if not domain:
            return ''

        return f'https://www.google.com/s2/favicons?domain={domain}&sz=64'

    def save(self, *args, **kwargs):
        if not self.short_code:
            while True:
                code = secrets.token_urlsafe(5)[:7]

                if not ShortLink.objects.filter(
                    short_code=code
                ).exists():
                    self.short_code = code
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title