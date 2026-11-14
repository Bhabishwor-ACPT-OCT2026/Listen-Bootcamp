import os
from uuid import uuid4
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from models import PodcastScript

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

def generate_audio(script: PodcastScript) -> str:
    text = script.script.strip()

    if not text:
        raise ValueError("The podcast script is empty.")

    client = OpenAI()

    output_folder = Path(__file__).resolve().parent / "outputs"
    output_folder.mkdir(exist_ok=True)

    audio_path = output_folder / f"podcast_{uuid4().hex}.mp3"
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="fable",
        input=text,
        instructions="Speak warmly and clearly, like a friendly podcast host.",
        response_format="mp3",
    ) as response:
        response.stream_to_file(audio_path)

    return str(audio_path)
if __name__ == "__main__":
    test_podcast = PodcastScript(
        title="Welcome to Listen Bootcamp",
        script=(
            "Welcome to Listen Bootcamp! Today we learn how Python "
            "turns our course notes into a podcast."
        ),
    )

    audio_path = generate_audio(test_podcast)
    print("Audio saved:", audio_path)