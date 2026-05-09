from openai import OpenAI

_SYSTEM_PROMPT = """You are a precise assistant that turns raw voice-note transcripts into structured notes.

Return your response in exactly this format (no markdown fences, plain text):

TITLE: <short title, max 8 words>

SUMMARY:
<2-4 sentence clean summary of the core idea>

NEXT ACTIONS:
- <action item>
- <action item>
(omit section if none)

REMINDERS / FOLLOW-UPS:
- <item>
(omit section if none)

ORIGINAL TRANSCRIPT:
<verbatim transcript>"""


def curate_transcript(transcript: str, api_key: str) -> dict:
    """Return a dict with keys: title, body (full formatted note)."""
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    text = response.choices[0].message.content.strip()
    title = _extract_title(text)
    return {"title": title, "body": text}


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.upper().startswith("TITLE:"):
            return line.split(":", 1)[1].strip()
    return "Voice Note"
