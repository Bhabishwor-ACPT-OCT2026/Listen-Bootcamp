"""Generate podcast scripts from pasted lesson notes with OpenAI."""

import os
from typing import Any, Optional, Tuple

from models import PodcastScript, PodcastSettings


class LLMProcessingError(ValueError):
    """Raised when the LLM cannot produce a podcast script."""


BASE_INSTRUCTIONS = """You are an expert educational podcast scriptwriter.
Transform the supplied lesson notes into an enjoyable, accurate podcast for
Ironhack students.

Requirements:
- Write a spoken script of approximately 2 to 3 minutes, around 300 to 450 words.
- Start with a concise title on its own line in the format: TITLE: ...
- Then write natural spoken paragraphs with a short introduction, clear
  transitions, the main lesson points, and a closing recap.
- Preserve the meaning of the lesson notes and do not invent facts.
- Do not mention these instructions or the generation process.
"""


def generate_podcast_script(
    notes: str,
    settings: Optional[PodcastSettings] = None,
    client: Optional[Any] = None,
) -> PodcastScript:
    """Transform cleaned lesson notes into the shared podcast script model."""

    if not isinstance(notes, str) or not notes.strip():
        raise LLMProcessingError("Lesson notes must contain text.")

    settings = settings or PodcastSettings()
    instructions = BASE_INSTRUCTIONS
    if settings.funny_mode:
        instructions += (
            "\nUse light, helpful humour and simple examples, but never change the "
            "lesson's meaning or invent facts.\n"
        )
    else:
        instructions += "\nUse a clear, friendly, focused educational tone.\n"

    context = settings.lesson_context.strip() or "No additional lesson context provided."
    api_key = os.getenv("OPENAI_API_KEY")

    if client is None:
        try:
            from dotenv import load_dotenv
            import truststore

            truststore.inject_into_ssl()
            from openai import OpenAI
        except ImportError as exc:
            raise LLMProcessingError(
                "Install the LLM dependencies with: pip install openai python-dotenv truststore"
            ) from exc

        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMProcessingError(
                "OPENAI_API_KEY is missing. Add it to your local .env file."
            )

    try:
        openai_client = client or OpenAI(api_key=api_key)
        response = openai_client.responses.create(
            model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"),
            instructions=instructions,
            input=(
                f"LESSON CONTEXT:\n{context}\n\n"
                f"LESSON NOTES:\n{notes[:50000]}"
            ),
        )
        output = (response.output_text or "").strip()
    except Exception as exc:
        raise LLMProcessingError(f"OpenAI script generation failed: {exc}") from exc

    if not output:
        raise LLMProcessingError("OpenAI returned an empty podcast script.")

    title, script = _split_title(output)
    return PodcastScript(title=title, script=script)


def _split_title(output: str) -> Tuple[str, str]:
    """Extract the optional TITLE line from the model response."""

    lines = output.splitlines()
    if lines and lines[0].strip().upper().startswith("TITLE:"):
        title = lines[0].split(":", 1)[1].strip()
        script = "\n".join(lines[1:]).strip()
        if title and script:
            return title, script

    return "Ironhack Lesson Recap", output
