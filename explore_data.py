import json

with open("data/tickets.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

print("Total tickets:", len(tickets))
print()
print("First ticket:")
print(tickets[0])