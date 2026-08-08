import json
import time
from task1_triage import triage_ticket, load_knowledge_base
from task2_summary import summarize_account

with open("data/tickets.json", "r", encoding="utf-8") as f:
    all_tickets = json.load(f)
with open("data/accounts.json", "r", encoding="utf-8") as f:
    all_accounts = json.load(f)

kb_text = load_knowledge_base()

results = []


def call_with_retry(func, *args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                print(f"Rate limited, waiting 30s... (attempt {attempt + 1})")
                time.sleep(30)
            else:
                raise


# ---- Task 1 test cases ----
task1_tests = [
    {"ticket": all_tickets[0], "expected_category": "Feature Request"},
    {"ticket": all_tickets[5], "expected_urgency": "P2"},
    {"ticket": all_tickets[10], "expected_field_present": "recommended_team"},
    {"ticket": all_tickets[20], "expected_field_present": "draft_reply"},
    {"ticket": {"subject": "help", "body": "it doesn't work"}, "expected_field_present": "urgency"},
]

for i, test in enumerate(task1_tests):
    try:
        time.sleep(15)
        output = call_with_retry(triage_ticket, test["ticket"], kb_text)
        passed = True
        notes = []

        if "expected_category" in test:
            passed = passed and (output.get("category") == test["expected_category"])
            notes.append(f"category={output.get('category')}")
        if "expected_urgency" in test:
            passed = passed and (output.get("urgency") == test["expected_urgency"])
            notes.append(f"urgency={output.get('urgency')}")
        if "expected_field_present" in test:
            passed = passed and (test["expected_field_present"] in output)
            notes.append(f"has_{test['expected_field_present']}={test['expected_field_present'] in output}")

        results.append({"task": "task1", "test_id": i, "pass": passed, "score": 1.0 if passed else 0.0, "notes": ", ".join(notes)})
    except Exception as e:
        results.append({"task": "task1", "test_id": i, "pass": False, "score": 0.0, "notes": f"ERROR: {e}"})

# ---- Task 2 test cases ----
task2_tests = [
    {"account_id": all_accounts[0]["account_id"], "expected_field_present": "executive_summary"},
    {"account_id": all_accounts[1]["account_id"], "expected_field_present": "risks_and_flags"},
    {"account_id": all_accounts[2]["account_id"], "expected_field_present": "talking_points"},
    {"account_id": all_accounts[3]["account_id"], "expected_min_risks": 1},
    {"account_id": "ACC-DOES-NOT-EXIST", "expected_error": True},
]

for i, test in enumerate(task2_tests):
    try:
        time.sleep(15)
        output = call_with_retry(summarize_account, test["account_id"], all_accounts, all_tickets)
        passed = True
        notes = []

        if "expected_error" in test:
            passed = "error" in output
            notes.append(f"handled_missing_account={passed}")
        if "expected_field_present" in test:
            passed = passed and (test["expected_field_present"] in output)
            notes.append(f"has_{test['expected_field_present']}={test['expected_field_present'] in output}")
        if "expected_min_risks" in test:
            passed = passed and (len(output.get("risks_and_flags", [])) >= test["expected_min_risks"])
            notes.append(f"num_risks={len(output.get('risks_and_flags', []))}")

        results.append({"task": "task2", "test_id": i, "pass": passed, "score": 1.0 if passed else 0.0, "notes": ", ".join(notes)})
    except Exception as e:
        results.append({"task": "task2", "test_id": i, "pass": False, "score": 0.0, "notes": f"ERROR: {e}"})

total = len(results)
passed_count = sum(1 for r in results if r["pass"])

report = {"summary": f"{passed_count}/{total} tests passed", "results": results}

with open("eval_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))