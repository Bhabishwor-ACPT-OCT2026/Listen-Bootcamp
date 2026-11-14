import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from models import PodcastScript

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

if __name__ == "__main__":
    print("OpenAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))

    client = OpenAI()

    output_folder = Path(__file__).resolve().parent / "outputs"
    output_folder.mkdir(exist_ok=True)

    test_script = (
        "Welcome to Listen Bootcamp! Today we learn how Python "
        "turns our course notes into a podcast."
    )

    audio_path = output_folder / "test_podcast.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="fable",
        input=test_script,
        instructions=(
            "Speak as an enthusiastic comedy podcast host. "
            "Use playful intonation and dramatic pauses. "
            "Keep technical terms clearly understandable."
        ),
        response_format="mp3",
    ) as response:
        response.stream_to_file(audio_path)

    print("Audio saved:", audio_path)