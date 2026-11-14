"""
main.py - Gradio UI for the Ironhack Podcast Studio.

Connects the pipeline:
    notes -> load_notes() -> generate_script() -> generate_audio() -> UI
"""

import tempfile
import wave
from pathlib import Path

import gradio as gr

from models import PodcastSettings, PodcastScript


# ============================================================
# PLACEHOLDERS
# These fake functions let us test the UI before the real
# modules are ready. Once they are, delete this block and use:
#
#   from data_processor import load_notes
#   from llm_processor import generate_script
#   from tts_generator import generate_audio
# ============================================================

def load_notes(raw_text: str) -> str:
    """Placeholder for Babishwor's version (cleans and validates the notes)."""
    return raw_text.strip()


def generate_script(text: str, settings: PodcastSettings) -> PodcastScript:
    """Placeholder for Babishwor's version (calls the LLM)."""
    mode = "funny" if settings.funny_mode else "normal"
    return PodcastScript(
        title="Test Episode",
        script=f"[{mode} mode] Placeholder script based on: {text[:100]}",
    )


def generate_audio(script: PodcastScript) -> str:
    """Placeholder for Angello's version (calls TTS).
    Writes one second of silence so the audio player has something to show."""
    path = Path(tempfile.gettempdir()) / "placeholder.wav"
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(24000)
        f.writeframes(b"\x00\x00" * 24000)
    return str(path)


# ============================================================
# PIPELINE
# Takes the raw values from the UI, runs all three steps and
# returns what the UI should display.
# ============================================================

def run_pipeline(raw_text: str, lesson_context: str, funny_mode: bool):
    if not raw_text or not raw_text.strip():
        raise gr.Error("Please paste your notes or a lesson transcript first.")

    try:
        settings = PodcastSettings(lesson_context=lesson_context, funny_mode=funny_mode)
        text = load_notes(raw_text)
        script = generate_script(text, settings)
        audio_path = generate_audio(script)
    except gr.Error:
        raise
    except Exception as e:
        raise gr.Error(f"Something went wrong: {e}")

    return script.title, script.script, audio_path


# ============================================================
# USER INTERFACE
# Left: inputs. Right: outputs.
# ============================================================

with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Ironhack Podcast Studio\nTurn your lesson notes into a short podcast.")

    with gr.Row():
        with gr.Column():
            notes_input = gr.Textbox(
                label="Lesson notes or transcript",
                lines=12,
                placeholder="Paste your notes or Zoom transcript here...",
            )
            context_input = gr.Textbox(
                label="Lesson context (optional)",
                placeholder="e.g. Week 4 - Python data structures",
            )
            funny_input = gr.Checkbox(
                label="Funny mode",
                info="Adds light humour and examples",
            )
            generate_btn = gr.Button("Generate podcast", variant="primary")

        with gr.Column():
            title_output = gr.Textbox(label="Title")
            script_output = gr.Textbox(label="Script", lines=12)
            audio_output = gr.Audio(label="Podcast", type="filepath")

    generate_btn.click(
        fn=run_pipeline,
        inputs=[notes_input, context_input, funny_input],
        outputs=[title_output, script_output, audio_output],
    )


if __name__ == "__main__":
    demo.launch()
