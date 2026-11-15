"""Convert text typed in the Preeti font into standard Nepali Unicode.

Preeti is not a real encoding. It draws Nepali letters on top of English keys,
so copied Preeti text looks like "g]kfn" instead of "नेपाल". Converting it takes
two stages:

1. Swap every Preeti key for its Nepali letter (CHAR_MAP).
2. Fix the order, because Preeti is typed in the order the letters are *drawn*,
   while Unicode stores them in the order they are *spoken*.
"""

import re

# Stage 1: Preeti key -> Nepali letter. A capital letter is usually the half
# form (with halant) of the lowercase one: s = क, S = क्.
CHAR_MAP = {
    # Number row
    "`": "ञ", "~": "ञ्", "1": "ज्ञ", "2": "द्द", "3": "घ", "4": "द्ध", "5": "छ",
    "6": "ट", "7": "ठ", "8": "ड", "9": "ढ", "0": "ण्",
    "!": "१", "@": "२", "#": "३", "$": "४", "%": "५", "^": "६", "&": "७",
    "*": "८", "(": "९", ")": "०", "-": "(", "_": ")", "=": ".", "+": "ं",
    # Top row
    "q": "त्र", "w": "ध", "e": "भ", "r": "च", "t": "त", "y": "थ", "u": "ग",
    "i": "ष्", "o": "य", "p": "उ", "[": "ृ", "]": "े", "\\": "्",
    "Q": "त्त", "W": "ध्", "E": "भ्", "R": "च्", "T": "त्", "Y": "थ्", "U": "ग्",
    "I": "क्ष्", "O": "इ", "P": "ए", "}": "ै", "|": "्र",
    # Home row
    "a": "ब", "s": "क", "d": "म", "f": "ा", "g": "न", "h": "ज", "j": "व",
    "k": "प", "l": "ि", ";": "स", "'": "ु",
    "A": "ब्", "S": "क्", "D": "म्", "F": "ँ", "G": "न्", "H": "ज्", "J": "व्",
    "K": "प्", "L": "ी", ":": "स्", '"': "ू",
    # Bottom row
    "z": "श", "x": "ह", "c": "अ", "v": "ख", "b": "द", "n": "ल",
    ",": ",", ".": "।", "/": "र",
    "Z": "श्", "X": "ह्", "C": "ऋ", "V": "ख्", "B": "द्य", "N": "ल्", "M": "ः",
    "<": "?", ">": "श्र", "?": "रु",
    # Extra symbols used for joined letters and punctuation
    "„": "ध्र", "…": "‘", "ˆ": "फ्", "‰": "झ्", "‹": "ङ्घ", "‘": "ॅ", "•": "ड्ड",
    "˜": "ऽ", "›": "द्र", "¡": "ज्ञ्", "¢": "द्घ", "£": "घ्", "¤": "झ्",
    "¥": "र्‍", "§": "ट्ट", "©": "र", "ª": "ङ", "«": "्र", "°": "ङ्ढ",
    "±": "+", "´": "झ", "¶": "ठ्ठ", "¿": "रू", "Å": "हृ", "Æ": "”", "Ë": "ङ्ग",
    "Ì": "न्न", "Í": "ङ्क", "Î": "ङ्ख", "Ö": "=", "×": "×", "Ø": "्य", "Ù": ";",
    "Ú": "’", "Û": "!", "Ü": "%", "Ý": "ट्ठ", "ß": "द्म", "å": "द्व", "æ": "“",
    "ç": "ॐ", "÷": "/",
}

# The "m" key is only a tail stroke: it turns the letter before it into another
# letter (प + tail = फ). A matra typed in between is kept.
TAIL_FORMS = {"k": "फ", "K": "फ्", "e": "झ", "p": "ऊ", "q": "क्र", "Q": "क्त", "j": "क"}
TAIL_PATTERN = re.compile(r"([kKepqQj])(['\"\[]?)m")

CONSONANT = "[क-ह]"
CLUSTER = f"{CONSONANT}(?:्‍?{CONSONANT})*"  # one letter or a joined group: क, प्र, स्त्र
MATRAS = "[ा-ौ]"
NASALS = "[ंँ]"
REPH = "{"  # the र् drawn on top of a letter, as in कार्य
DEVANAGARI = re.compile("[\u0900-\u097f]")


def preeti_to_unicode(text):
    """Return Preeti-typed text as Nepali Unicode. Line breaks are kept."""
    if not text:
        return ""

    # Real Preeti text has no Nepali letters in it. If we find any, the text is
    # already Unicode, and converting it would only damage its punctuation.
    if DEVANAGARI.search(text):
        return text

    # Tail stroke first, while the text is still Preeti keys.
    text = TAIL_PATTERN.sub(lambda m: TAIL_FORMS[m.group(1)] + m.group(2), text)

    # Stage 1: swap keys for letters. "{" and anything unknown pass through.
    text = "".join(CHAR_MAP.get(char, char) for char in text)

    # Stage 2: fix the order.
    # A half letter followed by aa is just the full letter: ण् + ा = ण.
    text = text.replace("्ा", "")

    # Short i is typed before its letter but stored after it: ि + क = कि.
    text = re.sub(f"ि({CLUSTER})", r"\1ि", text)

    # A matra typed before a joined ra or ya belongs after it: पे + ्र = प्रे.
    text = re.sub(f"({MATRAS}+)((?:्{CONSONANT})+)", r"\2\1", text)

    # Reph is typed after its syllable but stored before it: य + { = र्य.
    text = text.replace("इ" + REPH, "ई")
    text = re.sub(f"({CLUSTER})((?:{MATRAS}|{NASALS})*){re.escape(REPH)}", r"र्\1\2", text)

    # Nasal signs come after the matras: ं + ा = ा + ं.
    text = re.sub(f"({NASALS})({MATRAS}+)", r"\2\1", text)

    # Vowels that Preeti builds from pieces.
    text = text.replace("ेा", "ो").replace("ैा", "ौ")
    for pieces, vowel in (
        ("अाे", "ओ"), ("अाै", "औ"), ("अो", "ओ"), ("अौ", "औ"), ("अा", "आ"),
        ("एे", "ऐ"), ("ाे", "ो"), ("ाै", "ौ"),
    ):
        text = text.replace(pieces, vowel)

    # The M key is visarga (दुःख), but after a space it is used as a colon.
    text = re.sub(r"(^|\s)ः", r"\1:", text, flags=re.MULTILINE)

    return text
