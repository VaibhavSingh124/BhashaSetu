"""
BhashaSetu - Text Preprocessor (Task 4)
Cleans and normalises input text before it is sent to the translation model.

Design principles:
- Do NOT aggressively modify the user's text.
- Preserve sentence meaning and important punctuation.
- Keep preprocessing separate from the translation model.
"""

import re
import logging

logger = logging.getLogger(__name__)


def preprocess_text(text: str) -> str:
    """
    Normalise raw user input for translation.

    Steps performed (in order):
    1. Strip leading / trailing whitespace.
    2. Collapse multiple internal spaces into one.
    3. Normalise line endings to a single newline.
    4. Remove zero-width and invisible Unicode control characters.
    5. Ensure the text ends without a trailing newline.

    Parameters
    ----------
    text : str
        Raw user-supplied input string.

    Returns
    -------
    str
        Cleaned text ready for language validation and model inference.
    """
    if not text:
        return text

    # 1. Strip outer whitespace
    cleaned = text.strip()

    # 2. Remove zero-width / invisible control characters (U+200B, U+200C, U+FEFF …)
    cleaned = re.sub(r"[\u200b\u200c\u200d\ufeff\u00ad]", "", cleaned)

    # 3. Normalise line endings
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

    # 4. Collapse consecutive blank lines into one
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # 5. Collapse multiple spaces on the same line into one space
    cleaned = re.sub(r"[ \t]+", " ", cleaned)

    # 6. Strip trailing whitespace from each line
    cleaned = "\n".join(line.rstrip() for line in cleaned.split("\n"))

    logger.debug("Preprocessed text: %r → %r", text[:60], cleaned[:60])
    return cleaned


def is_text_empty(text: str) -> bool:
    """Return True if text is blank after preprocessing."""
    return not preprocess_text(text)
