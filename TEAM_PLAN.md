# Ironhack Podcast Studio — Team Plan

## Goal

Turn Ironhack course notes or Zoom lesson transcripts into an
enjoyable educational podcast that students can listen to while
doing other activities.

Presentation: Tuesday, 17 November 2026.
Format: 5–7 minutes, followed by 2–3 minutes of Q&A.

## First working version

The user:
1. Pastes notes or a lesson transcript.
2. Adds optional lesson context.
3. Chooses whether to enable funny mode.
4. Clicks Generate.
5. Receives the podcast title, script and playable/downloadable audio.

Start with one narrator and one audio file.
Aim for a short podcast of approximately 2–3 minutes.

Funny mode adds light humour and helpful examples.
It must preserve the meaning of the lesson and avoid invented facts.

For now, users paste text. Website retrieval, PDF uploads,
multiple speakers and special voice effects are optional later additions.

## Team responsibilities

| Person | Files | Responsibility |
|---|---|---|
| Babishwor | data_processor.py, llm_processor.py | Validate/clean notes and generate the podcast script |
| Angello | tts_generator.py | Generate and save audio; return its file path |
| Moritz | main.py | Build Gradio and connect the pipeline |

Agree on changes to models.py together.
One person should make each agreed change to avoid conflicting edits.

## Project structure

podcast-studio/
├── src/
│   ├── main.py
│   ├── models.py
│   ├── data_processor.py
│   ├── llm_processor.py
│   └── tts_generator.py
├── examples/
│   └── lesson_notes.txt
├── outputs/
├── requirements.txt
├── README.md
├── TEAM_PLAN.md
├── .gitignore
└── .env

.env is local and must never be committed.
Keep an example generated MP3 for the presentation/submission.

## Shared models — models.py

Use these exact class and field names:

```python
from pydantic import BaseModel, Field


class PodcastSettings(BaseModel):
    lesson_context: str = ""
    funny_mode: bool = False


class PodcastScript(BaseModel):
    title: str = Field(min_length=1)
    script: str = Field(min_length=1)
