"""
main.py - Gradio UI for the Ironhack Podcast Studio.

Connects the pipeline:
    notes -> clean_notes() -> generate_podcast_script() -> generate_audio() -> UI
"""

import gradio as gr

from models import PodcastSettings
from data_processor import clean_notes, DataProcessingError
from llm_processor import generate_podcast_script, LLMProcessingError
from tts_generator import generate_audio


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
        text = clean_notes(raw_text)
        script = generate_podcast_script(text, settings)
        audio_path = generate_audio(script)
    except gr.Error:
        raise
    except DataProcessingError as e:
        raise gr.Error(str(e))
    except LLMProcessingError as e:
        raise gr.Error(str(e))
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
