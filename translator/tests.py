from django.test import SimpleTestCase

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
