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
            "rows": 12,
            "maxlength": 5000,
            "placeholder": "Paste your letter or text here...",
        }),
    )
    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES, widget=forms.RadioSelect, initial="en_ne",
    )
    tone = forms.ChoiceField(
        choices=TONE_CHOICES, widget=forms.RadioSelect, initial="formal",
    )
    is_preeti = forms.BooleanField(
        required=False,
        label="My text is typed in Preeti font",
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("is_preeti") and cleaned_data.get("direction") != "ne_en":
            self.add_error(
                "is_preeti",
                "Preeti text is Nepali, so please choose Nepali → English.",
            )
        return cleaned_data


class EditTranslationForm(forms.Form):
    translated_text = forms.CharField(max_length=20000)

    def clean_translated_text(self):
        # Browsers send Windows line endings; store plain ones.
        return self.cleaned_data["translated_text"].replace("\r\n", "\n")


class PreetiForm(forms.Form):
    text = forms.CharField(
        max_length=10000,
        widget=forms.Textarea(attrs={
            "rows": 12,
            "maxlength": 10000,
            "placeholder": "Paste Preeti text here, for example: g]kfn ;/sf/",
        }),
    )
