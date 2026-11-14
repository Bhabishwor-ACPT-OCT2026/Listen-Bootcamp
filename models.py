
"""Shared Pydantic models for the Podcast Studio team pipeline."""

from pydantic import BaseModel, Field


class PodcastSettings(BaseModel):
    """Optional settings supplied by the user through the Gradio interface."""

    lesson_context: str = ""
    funny_mode: bool = False


class PodcastScript(BaseModel):
    """Podcast script returned by the LLM processing stage."""

    title: str = Field(min_length=1)
    script: str = Field(min_length=1)
