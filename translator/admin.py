from django.contrib import admin

from .models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ("user", "direction", "tone", "short_source", "created_at")
    list_filter = ("direction", "tone", "created_at")
    search_fields = ("source_text", "translated_text", "user__username")
    readonly_fields = ("created_at",)

    @admin.display(description="Source text")
    def short_source(self, obj):
        return obj.source_text[:50] + ("..." if len(obj.source_text) > 50 else "")
