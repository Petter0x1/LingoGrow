import re
from bidi.algorithm import get_display
from arabic_reshaper import reshape


def reshape_arabic(text):
    """Reshape Arabic text for proper display."""
    reshaped_text = reshape(text)
    return get_display(reshaped_text)


def normalize_arabic(text):
    """Normalize Arabic text by removing diacritics and standardizing characters."""
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'[ى]', 'ي', text)
    text = re.sub(r'[ؤئ]', 'ء', text)
    text = re.sub(r'[ً-ْ]', '', text)  # remove diacritics
    return text.strip().lower()