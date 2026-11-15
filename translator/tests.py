from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from .models import Translation
from .preeti import preeti_to_unicode


class PreetiToUnicodeTests(SimpleTestCase):
    def assertConverts(self, preeti, expected):
        self.assertEqual(preeti_to_unicode(preeti), expected)

    def test_simple_words(self):
        self.assertConverts("g]kfn", "नेपाल")
        self.assertConverts(";/sf/", "सरकार")
        self.assertConverts("gful/stf", "नागरिकता")

    def test_short_i_moves_after_its_letter(self):
        self.assertConverts("lgj]bg", "निवेदन")
        self.assertConverts("lk|o", "प्रिय")
        self.assertConverts("/fli6«o", "राष्ट्रिय")

    def test_reph_moves_before_its_letter(self):
        self.assertConverts("sfof{no", "कार्यालय")
        self.assertConverts("ljBfyL{", "विद्यार्थी")
        self.assertConverts("ug'{", "गर्नु")

    def test_tail_stroke_letters(self):
        self.assertConverts("l;kmfl/;", "सिफारिस")
        self.assertConverts("zlQm", "शक्ति")
        self.assertConverts("em08f", "झण्डा")

    def test_built_up_vowels(self):
        self.assertConverts("cfof]u", "आयोग")
        self.assertConverts("cf}iflw", "औषधि")
        self.assertConverts("O{Zj/", "ईश्वर")

    def test_half_letters_and_conjuncts(self):
        self.assertConverts("x'G5", "हुन्छ")
        self.assertConverts("lzIff", "शिक्षा")
        self.assertConverts("5fqj[lQ", "छात्रवृत्ति")

    def test_digits_and_punctuation(self):
        self.assertConverts("j8f g+= $", "वडा नं. ४")
        self.assertConverts("ldlt M @)*#", "मिति : २०८३")
        self.assertConverts("b'Mv", "दुःख")

    def test_keeps_line_breaks(self):
        self.assertConverts("ljifo\nlgj]bg", "विषय\nनिवेदन")

    def test_unicode_nepali_is_left_alone(self):
        self.assertConverts("मिति: २०८३-०७-२९", "मिति: २०८३-०७-२९")

    def test_empty_text(self):
        self.assertConverts("", "")


class EditTranslationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="pass12345")
        self.other = User.objects.create_user("other", password="pass12345")
        self.translation = Translation.objects.create(
            user=self.owner,
            source_text="Seema Singdan",
            translated_text="सीमा सिङ्दान",
            direction="en_ne",
            tone="formal",
        )
        self.edit_url = f"/history/{self.translation.pk}/edit/"

    def test_owner_can_fix_the_translation(self):
        self.client.login(username="owner", password="pass12345")
        self.client.post(self.edit_url, {"translated_text": "सीमा सिङदन"})
        self.translation.refresh_from_db()
        self.assertEqual(self.translation.translated_text, "सीमा सिङदन")

    def test_other_user_cannot_edit(self):
        self.client.login(username="other", password="pass12345")
        response = self.client.post(self.edit_url, {"translated_text": "changed"})
        self.assertEqual(response.status_code, 404)
        self.translation.refresh_from_db()
        self.assertEqual(self.translation.translated_text, "सीमा सिङ्दान")

    def test_empty_edit_is_not_saved(self):
        self.client.login(username="owner", password="pass12345")
        self.client.post(self.edit_url, {"translated_text": "   "})
        self.translation.refresh_from_db()
        self.assertEqual(self.translation.translated_text, "सीमा सिङ्दान")

    def test_download_uses_the_edited_text(self):
        self.client.login(username="owner", password="pass12345")
        download_url = f"/history/{self.translation.pk}/download/"
        response = self.client.post(download_url, {"translated_text": "सीमा सिङदन"})
        self.assertEqual(response.status_code, 200)
        self.translation.refresh_from_db()
        self.assertEqual(self.translation.translated_text, "सीमा सिङदन")
