from django.conf import settings
from django.db import models


class Translation(models.Model):
    DIRECTION_CHOICES = [
        ("en_ne", "English → Nepali"),
        ("ne_en", "Nepali → English"),
    ]
    TONE_CHOICES = [
        ("formal", "Formal / Official"),
        ("simple", "Simple"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    source_text = models.TextField()
    translated_text = models.TextField()
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    tone = models.CharField(max_length=10, choices=TONE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_direction_display()} - {self.created_at:%Y-%m-%d %H:%M}"
