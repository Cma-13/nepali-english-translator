from io import BytesIO

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

# Nirmala UI ships with Windows and covers both Devanagari and English.
FONT_NAME = "Nirmala UI"
FONT_SIZE = Pt(12)


def _apply_font(run):
    """Set the font for every script, so Word doesn't swap in a font that breaks Nepali."""
    run.font.name = FONT_NAME
    run.font.size = FONT_SIZE
    fonts = run._element.get_or_add_rPr().get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(attr), FONT_NAME)


def build_translation_docx(translation):
    """Return the translated text as a .docx file (bytes), keeping every line break."""
    document = Document()

    for line in translation.translated_text.splitlines():
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(4)
        _apply_font(paragraph.add_run(line))

    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()
