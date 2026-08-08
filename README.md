# Zycus AI Engineer Intern — Task Submission

AI-powered support ticket triage and account health summarization system, built with Python and Google Gemini.

## Setup

1. Clone this repo and navigate into it:
```
   git clone https://github.com/kavi8422/zycus-AI-Engineer-task-.git
   cd zycus-AI-Engineer-task-
```

2. Create a virtual environment and activate it:
```
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate   # Mac/Linux
```

3. Install dependencies:
```
   pip install google-genai python-dotenv
```

4. Create a `.env` file in the project root (see `.env.example`) with your own Google Gemini API key:
```
   GOOGLE_API_KEY=your_key_here
```
   Get a free key at https://aistudio.google.com/apikey

## How to Run

**Task 1 — Ticket Triage:**
```
python task1_triage.py
```
Classifies a sample ticket into product area, category, and urgency (P1–P4), matches it against the knowledge base, and drafts a first-response reply.

**Task 2 — Account Health Summary:**
```
python task2_summary.py
```
Generates an executive summary, risk flags (with quoted evidence), and talking points for a sample customer account.

**Task 3 — Evaluation Harness:**
```
python task3_evals.py
```
Runs 10 automated test cases (5 per task, including one adversarial case each) and saves results to `eval_report.json`.

## Sample Output

Task 1 (triage) returns structured JSON like:
```json
{
  "product_area": "DataBridge Pro",
  "category": "Feature Request",
  "urgency": "P3",
  "reasoning": "...",
  "matched_kb_source": null,
  "recommended_team": "DataBridge Pro Product Team",
  "draft_reply": "..."
}
```

Task 3 (evals) produces a report like:
```json
{
  "summary": "10/10 tests passed",
  "results": [...]
}
```

## Design Note

See [DESIGN_NOTE.md](DESIGN_NOTE.md) for a discussion of failure modes, the latency/quality
trade-off made, PII handling, and scaling considerations.

## Notes

- Uses Google Gemini (`gemini-flash-latest`) via the free tier.
- Free tier is rate-limited to 5 requests/minute — `task3_evals.py` includes automatic
  retry-with-backoff and spacing between calls to handle this gracefully.
- All data used is the synthetic dataset provided in this repo (`data/`, `knowledge-base/`).