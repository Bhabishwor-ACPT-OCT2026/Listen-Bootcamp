"""Validate and clean pasted lesson notes."""

import re


class DataProcessingError(ValueError):
    """Raised when lesson notes cannot be processed."""


def clean_notes(raw_text: str) -> str:
    if not isinstance(raw_text, str):
        raise DataProcessingError("Lesson notes must be provided as text.")

    normalized = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned_lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in normalized.split("\n")
    ]

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    if not cleaned:
        raise DataProcessingError("Please paste lesson notes.")

    return cleaned