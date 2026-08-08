import os
import json
from datetime import datetime, timedelta, timezone
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_account_tickets(account_id, tickets, days=90):
    """Returns tickets for one account from the last N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [
        t for t in tickets
        if t["account_id"] == account_id
        and datetime.fromisoformat(t["created_at"].replace("Z", "+00:00")) > cutoff
    ]


def summarize_account(account_id, accounts, tickets):
    """Takes an account_id, returns a structured health brief."""

    # Find the account record
    account = next((a for a in accounts if a["account_id"] == account_id), None)
    if account is None:
        return {"error": f"No account found with id {account_id}"}

    # Get their recent tickets
    recent_tickets = get_account_tickets(account_id, tickets, days=90)
    tickets_text = "\n".join(
        f"- [{t['ticket_id']}] ({t['urgency']}) {t['subject']}: {t['body'][:200]}"
        for t in recent_tickets
    )

    prompt = f"""
You are a TAM (Technical Account Manager) assistant preparing a pre-call brief.

ACCOUNT DATA:
{json.dumps(account, indent=2)}

RECENT TICKETS (last 90 days):
{tickets_text if tickets_text else "No tickets in the last 90 days."}

Produce a brief with ONLY valid JSON in this exact format:
{{
  "executive_summary": "3-5 sentences",
  "risks_and_flags": [
    {{"risk": "description", "evidence_quote": "direct quote from a ticket or escalation note"}}
  ],
  "talking_points": ["point 1", "point 2", "..."]
}}
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    config={"temperature": 0, "seed": 42}
)

    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    return json.loads(raw_text)


if __name__ == "__main__":
    with open("data/accounts.json", "r", encoding="utf-8") as f:
        accounts = json.load(f)
    with open("data/tickets.json", "r", encoding="utf-8") as f:
        tickets = json.load(f)

    test_account_id = accounts[0]["account_id"]
    result = summarize_account(test_account_id, accounts, tickets)
    print(json.dumps(result, indent=2))