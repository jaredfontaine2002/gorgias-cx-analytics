"""Generate a synthetic Gorgias ticket export for a bike shop.

Produces data/tickets.csv with one row per ticket:
    ticket_id, created_at, first_response_at, resolved_at,
    channel, tag, agent, csat_score, subject

Tags are bike-shop specific: sizing, shipping, returns, warranty,
compatibility, order-status, stock.

Run:  python data/generate_tickets.py
"""
import csv
import random
from datetime import datetime, timedelta

SEED = 7
N_TICKETS = 900
START = datetime(2025, 1, 1)
OUTFILE = "data/tickets.csv"

random.seed(SEED)

TAGS = {
    "sizing":        {"weight": 0.22, "resolve_h": (2, 30),  "csat": (3.6, 4.8)},
    "shipping":      {"weight": 0.18, "resolve_h": (4, 72),  "csat": (3.2, 4.5)},
    "order-status":  {"weight": 0.16, "resolve_h": (1, 12),  "csat": (4.0, 4.9)},
    "returns":       {"weight": 0.14, "resolve_h": (6, 96),  "csat": (3.0, 4.4)},
    "compatibility": {"weight": 0.12, "resolve_h": (3, 48),  "csat": (3.8, 4.9)},
    "warranty":      {"weight": 0.10, "resolve_h": (12, 120), "csat": (3.1, 4.3)},
    "stock":         {"weight": 0.08, "resolve_h": (2, 24),  "csat": (3.9, 4.8)},
}

CHANNELS = ["email", "chat", "phone", "sms"]
CHANNEL_W = [0.45, 0.30, 0.15, 0.10]
AGENTS = ["Maya", "Leo", "Priya", "Sam", "Nora"]

SUBJECTS = {
    "sizing": ["What size frame for 5'11\"?", "Sizing help: road bike",
               "Between M and L — which one?"],
    "shipping": ["Where is my order?", "Tracking hasn't updated",
                 "Delivery delayed"],
    "order-status": ["Order confirmation question", "Can I change my order?",
                     "Payment issue at checkout"],
    "returns": ["How do I start a return?", "Return label not working",
                "Refund status"],
    "compatibility": ["Will this groupset fit my frame?",
                      "12-speed chain on 11-speed cassette?",
                      "Disc brake adapter question"],
    "warranty": ["Cracked rim — warranty?", "Warranty claim status",
                 "Crash replacement options"],
    "stock": ["When is the Tarmac back in stock?", "Restock ETA?",
              "Notify me when available"],
}


def pick_tag() -> str:
    r = random.random()
    cum = 0.0
    for tag, spec in TAGS.items():
        cum += spec["weight"]
        if r < cum:
            return tag
    return "sizing"


def main() -> None:
    rows = []
    for i in range(1, N_TICKETS + 1):
        tag = pick_tag()
        spec = TAGS[tag]
        created = START + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59))
        # first response: faster on chat, slower on email
        channel = random.choices(CHANNELS, weights=CHANNEL_W)[0]
        frt_h = {"chat": (0.1, 2), "sms": (0.2, 3),
                 "phone": (0.05, 0.5), "email": (1, 10)}[channel]
        first_response = created + timedelta(
            hours=random.uniform(*frt_h))
        resolved = first_response + timedelta(
            hours=random.uniform(*spec["resolve_h"]))
        lo, hi = spec["csat"]
        csat = round(random.uniform(lo, hi), 1) if random.random() < 0.62 else ""
        rows.append([i, created.isoformat(timespec="minutes"),
                     first_response.isoformat(timespec="minutes"),
                     resolved.isoformat(timespec="minutes"),
                     channel, tag, random.choice(AGENTS), csat,
                     random.choice(SUBJECTS[tag])])

    with open(OUTFILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticket_id", "created_at", "first_response_at",
                    "resolved_at", "channel", "tag", "agent",
                    "csat_score", "subject"])
        w.writerows(rows)
    print(f"Wrote {len(rows):,} tickets to {OUTFILE}")


if __name__ == "__main__":
    main()
