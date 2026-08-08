import os
import json
import glob
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def load_knowledge_base():
    """Reads every .md file in knowledge-base/ and combines them into one text block."""
    kb_chunks = []
    for filepath in glob.glob("knowledge-base/**/*.md", recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        kb_chunks.append(f"### Source: {filepath}\n{content}")
    return "\n\n".join(kb_chunks)


def triage_ticket(ticket, kb_text):
    """Takes one ticket dict, returns a structured triage result."""

    prompt = f"""
You are a support ticket triage assistant for an enterprise software company.

KNOWLEDGE BASE (for reference):
{kb_text[:8000]}

TICKET TO TRIAGE:
Subject: {ticket['subject']}
Body: {ticket['body']}

Respond with ONLY valid JSON in this exact format, no extra text:
{{
  "product_area": "...",
  "category": "...",
  "urgency": "P1, P2, P3, or P4",
  "reasoning": "...",
  "matched_kb_source": "filename or null if no match",
  "recommended_team": "...",
  "draft_reply": "a short, professional first-response message to the customer"
}}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    # Clean up the response in case Gemini wraps it in ```json ... ```
    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    return json.loads(raw_text)


if __name__ == "__main__":
    with open("data/tickets.json", "r", encoding="utf-8") as f:
        tickets = json.load(f)

    kb_text = load_knowledge_base()

    result = triage_ticket(tickets[5], kb_text)
    print(json.dumps(result, indent=2))