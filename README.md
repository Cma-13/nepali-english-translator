# Nepali ↔ English Letter Translator

A web app that translates **official letters** between Nepali and English: applications (निवेदन), recommendation letters (सिफारिस), notices and office letters.

General translators are made for understanding text. This one is made for a specific job: getting a letter ready to hand in at a ward office, college or company. So it keeps the formal tone and the letter layout, reads old Preeti-font documents, and gives you a Word file at the end.

## Features

- **Formal letter translation** in both directions, with a Formal or Simple tone. The date, subject (विषय), greeting and signature lines stay where they were.
- **Preeti → Unicode converter.** Many old Nepali documents are typed in the Preeti font, which turns into text like `g]kfn` when copied. The app converts it to real Nepali (नेपाल) and can translate it in the same step.
- **Editable result.** Fix a name or a word directly on the translated letter before you copy or download it.
- **Word download.** Any translation can be downloaded as a `.docx` file with the line breaks kept.
- **History per user.** Every translation is saved to the account that made it. Users can view, edit and delete only their own.
- **REST API** with token login, so another app can use the translator.
- **Works on phones.** Every page adapts to small screens.

## Tech stack

| Part | What is used |
|---|---|
| Backend | Python, Django 6 |
| API | Django REST Framework (token and session login, throttling, pagination) |
| AI | Google Gemini (Flash model) through the `google-genai` library |
| Word files | `python-docx` |
| Database | SQLite |
| Frontend | Django templates, plain CSS and JavaScript (no framework) |

## How a translation works

1. The user pastes a letter and picks the direction and tone.
2. If the Preeti option is ticked, `translator/preeti.py` converts the text to Unicode first.
3. `translator/services.py` sends the text to Gemini with a system prompt written for official letters. All AI code lives in this one file, so the provider can be swapped without touching the views.
4. The result is saved as a `Translation` row linked to the user, then shown on an editable sheet.
5. Copy and Download Word always use the text on screen, including the user's edits.

If Gemini is down or the free limit is reached, the user sees a plain message instead of an error page.

## Run it on your computer

You need Python 3.12 or newer and a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

```bash
git clone https://github.com/Cma-13/nepali-translator.git
cd nepali-translator

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

pip install -r requirements.txt
```

Copy `.env.example` to a new file named `.env` and fill in your key:

```
SECRET_KEY=any-long-random-text
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Then set up the database and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ and create an account.

## API

Every endpoint needs a login. Get a token first, then send it in the `Authorization` header.

| Method | Endpoint | What it does |
|---|---|---|
| POST | `/api/token/` | Send username and password, get a token |
| POST | `/api/translate/` | Translate text and save it to history |
| POST | `/api/preeti/` | Convert Preeti text to Unicode |
| GET | `/api/history/` | List your translations, 10 per page |
| GET | `/api/history/<id>/` | View one translation |
| PATCH | `/api/history/<id>/` | Correct the translated text |
| DELETE | `/api/history/<id>/` | Delete one translation |

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/translate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "I would like to request a recommendation letter.", "direction": "en_ne", "tone": "formal"}'
```

`direction` is `en_ne` or `ne_en`. `tone` is `formal` or `simple`. Add `"is_preeti": true` to convert Preeti text before translating. Translation requests are limited to 10 per minute per user.

## Tests

```bash
python manage.py test translator
```

The tests cover the Preeti converter (word order rules, joined letters, digits and punctuation) and editing a translation (only the owner can edit, empty edits are rejected, downloads use the edited text).

## Project structure

```
config/                 Project settings and main URLs
accounts/               Sign up, log in, log out
translator/
    services.py         Gemini call and the system prompt
    preeti.py           Preeti to Unicode converter
    documents.py        Builds the Word file
    models.py           Translation model
    views.py            Web pages
    api.py              REST API views
    serializers.py      API input and output
    tests.py            Automated tests
templates/              HTML pages
static/                 CSS, JavaScript and the tab icon
```

## What I learned while building it

- **Prompt rules must be clear.** An early rule said "keep numbers as they are". The model could not tell whether that included Nepali digits, and it started writing its reasoning into the letter. Splitting it into two exact rules (keep the same calendar, use Nepali digits in Nepali output) fixed it.
- **The model adds things.** It translated "resident" as "permanent resident" (स्थायी बासिन्दा), which means something different at a ward office. A rule with that exact example stopped it.
- **Some problems are not prompt problems.** A name can be written several ways in Devanagari, and only the owner knows the right one. No prompt can fix that, so the result is editable instead.
- **Test with wrong input too.** Ticking the Preeti option on text that was already Unicode damaged its punctuation (`:` is a Preeti key for स्). The converter now skips text that already contains Nepali letters, and a test keeps that bug from coming back.

## Known limits

- Translations come from an AI model. Names, dates and numbers should be checked before a letter is submitted.
- English words inside Preeti text cannot be told apart from Preeti keys, so they get converted too.
- The app uses Gemini's free tier, where submitted text may be used by Google to improve its products. Do not paste citizenship numbers or other private IDs.


## Author

Seema Singdan, [github.com/Cma-13](https://github.com/Cma-13)
