from rest_framework import serializers

from .models import Translation


class TranslateRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)
    direction = serializers.ChoiceField(choices=Translation.DIRECTION_CHOICES)
    tone = serializers.ChoiceField(choices=Translation.TONE_CHOICES, default="formal")
    is_preeti = serializers.BooleanField(default=False)

    def validate(self, data):
        if data["is_preeti"] and data["direction"] != "ne_en":
            raise serializers.ValidationError(
                {"is_preeti": "Preeti text is Nepali, so direction must be ne_en."}
            )
        return data


class PreetiRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10000)


class TranslationSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(source="get_direction_display", read_only=True)
    tone_display = serializers.CharField(source="get_tone_display", read_only=True)

    class Meta:
        model = Translation
        fields = [
            "id",
            "source_text",
            "translated_text",
            "direction",
            "direction_display",
            "tone",
            "tone_display",
            "created_at",
        ]
        # Only the translated text can be corrected after saving.
        read_only_fields = [f for f in fields if f != "translated_text"]
