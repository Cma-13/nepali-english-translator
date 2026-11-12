from django import forms


class TranslateForm(forms.Form):
    DIRECTION_CHOICES = [
        ("en_ne", "English → Nepali"),
        ("ne_en", "Nepali → English"),
    ]
    TONE_CHOICES = [
        ("formal", "Formal / Official"),
        ("simple", "Simple"),
    ]

    text = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(attrs={
            "rows": 10,
            "placeholder": "Paste your letter or text here...",
        }),
    )
    direction = forms.ChoiceField(choices=DIRECTION_CHOICES)
    tone = forms.ChoiceField(choices=TONE_CHOICES)