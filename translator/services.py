import os

from google import genai
from google.genai import errors, types

LANGUAGES = {
    "en_ne": ("English", "Nepali"),
    "ne_en": ("Nepali", "English"),
}

TONE_RULES = {
    "formal": (
        "Use a formal, official tone suitable for government offices, ward offices, "
        "colleges and companies. In Nepali, use standard official letter phrases "
        "(for example: श्रीमान्, उपरोक्त विषयमा, अनुरोध गर्दछु, गरिदिनुहुन, भवदीय)."
    ),
    "simple": "Use clear, simple, everyday language while staying polite.",
}

SYSTEM_PROMPT = """You are a professional translator for official Nepali and English documents
such as applications (निवेदन), recommendation letters (सिफारिस), notices and office letters.

Strict rules:
1. Output ONLY the final translated text. Never include notes, explanations, reasoning,
   options, pronunciation, brackets with comments, or quotes.
2. Keep the original structure exactly: line breaks, date, subject (विषय), salutation,
   body, closing and signature.
3. Nepali output must use standard Devanagari Unicode only. Never use characters
   from any other script.
4. Dates: keep the same calendar as the source. Never convert AD dates to Bikram Sambat
   (BS) or BS to AD.
5. Digits: in Nepali output, write every number with Nepali digits (०१२३४५६७८९),
   including dates and ward numbers. In English output, use 0-9.
6. Personal names: transliterate them by sound into the target script, carefully and
   consistently (for example: Singdan → सिङदन, Sharma → शर्मा).
7. Translate the meaning naturally, using phrases a Nepali government office would
   actually use, not word by word."""


class TranslationError(Exception):
    """Raised with a user-friendly message when translation fails."""


def translate_text(text, direction, tone):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise TranslationError("Translation service is not set up yet. Please try again later.")

    source, target = LANGUAGES[direction]
    prompt = (
        f"Translate the following text from {source} to {target}.\n"
        f"Tone: {TONE_RULES[tone]}\n\n"
        f"Text:\n{text}"
    )

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
            ),
        )
    except errors.APIError as e:
        if e.code == 429:
            raise TranslationError("Too many requests right now. Please wait a minute and try again.")
        raise TranslationError("The translation service is having trouble. Please try again shortly.")
    except Exception:
        raise TranslationError("Could not reach the translation service. Check your internet and try again.")

    result = (response.text or "").strip()
    if not result:
        raise TranslationError("No translation came back. Please try again.")
    return result