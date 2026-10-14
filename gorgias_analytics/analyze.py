"""CX analytics for a bike shop's Gorgias ticket export.

Reads data/tickets.csv and computes the metrics a Gorgias Admin watches:
first response time, resolution time, CSAT, SLA breaches, volume by
channel/tag/agent/hour. Saves charts to charts/ and writes REPORT.md.

Run:  python gorgias_analytics/analyze.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tickets.csv"
CHARTS = ROOT / "charts"
REPORT = ROOT / "REPORT.md"

# Gorgias-style SLA targets for a bike shop
FRT_SLA_HOURS = 4      # first response within 4 business hours
RES_SLA_HOURS = 48     # resolved within 48 hours


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["created_at", "first_response_at",
                                        "resolved_at"])
    df["frt_hours"] = (df["first_response_at"] - df["created_at"]).dt.total_seconds() / 3600
    df["resolve_hours"] = (df["resolved_at"] - df["first_response_at"]).dt.total_seconds() / 3600
    df["hour"] = df["created_at"].dt.hour
    df["weekday"] = df["created_at"].dt.day_name()
    df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")
    return df


def chart(df: pd.DataFrame) -> None:
    CHARTS.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby("tag")["frt_hours"].median().sort_values().plot.barh(ax=ax, color="#2a7f62")
    ax.set_xlabel("Median hours")
    ax.set_title("Median first response time by ticket tag")
    fig.tight_layout()
    fig.savefig(CHARTS / "frt_by_tag.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby("tag")["csat_score"].mean().sort_values().plot.barh(ax=ax, color="#3b6ea5")
    ax.set_xlabel("Mean CSAT (1-5)")
    ax.set_title("CSAT by ticket tag")
    fig.tight_layout()
    fig.savefig(CHARTS / "csat_by_tag.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby("hour").size().plot(ax=ax, color="#c96a2b")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Tickets")
    ax.set_title("Ticket volume by hour — staff the peaks")
    fig.tight_layout()
    fig.savefig(CHARTS / "volume_by_hour.png")
    plt.close(fig)

    print(f"Charts saved to {CHARTS}/")


def summarize(df: pd.DataFrame) -> dict:
    rated = df.dropna(subset=["csat_score"])
    return {
        "tickets": len(df),
        "median_frt": df["frt_hours"].median(),
        "median_resolve": df["resolve_hours"].median(),
        "csat": rated["csat_score"].mean(),
        "csat_n": len(rated),
        "frt_breach": (df["frt_hours"] > FRT_SLA_HOURS).mean(),
        "res_breach": (df["resolve_hours"] > RES_SLA_HOURS).mean(),
        "by_channel": df.groupby("channel").size().sort_values(ascending=False),
        "by_tag": df.groupby("tag").size().sort_values(ascending=False),
        "csat_by_tag": rated.groupby("tag")["csat_score"].mean().sort_values(),
        "frt_by_tag": df.groupby("tag")["frt_hours"].median().sort_values(ascending=False),
        "by_agent": df.groupby("agent").agg(tickets=("ticket_id", "size"),
                                            csat=("csat_score", "mean")),
        "peak_hour": df.groupby("hour").size().idxmax(),
    }


def main() -> None:
    df = load()
    s = summarize(df)
    chart(df)

    worst_tag = s["csat_by_tag"].idxmin()
    slowest_tag = s["frt_by_tag"].idxmax()

    report = f"""# Gorgias CX Report — Bike Shop (synthetic data)

- **Tickets analyzed:** {s['tickets']:,}
- **Median first response:** {s['median_frt']:.1f}h (SLA {FRT_SLA_HOURS}h — breach rate {s['frt_breach']:.1%})
- **Median resolution:** {s['median_resolve']:.1f}h (SLA {RES_SLA_HOURS}h — breach rate {s['res_breach']:.1%})
- **CSAT:** {s['csat']:.2f}/5 across {s['csat_n']:,} rated tickets
- **Peak hour:** {s['peak_hour']}:00 — schedule coverage here first

## Volume by channel
{s['by_channel'].to_markdown()}

## Volume by tag
{s['by_tag'].to_markdown()}

## CSAT by tag (lowest first)
{s['csat_by_tag'].apply(lambda x: f"{x:.2f}").to_markdown()}

## Median first response by tag (slowest first)
{s['frt_by_tag'].apply(lambda x: f"{x:.1f}h").to_markdown()}

## Agent scorecard
{s['by_agent'].round(2).to_markdown()}

## Recommendations
1. **'{worst_tag}'** has the lowest CSAT ({s['csat_by_tag'].min():.2f}) — build
   Gorgias macros + a help-center article for the top '{worst_tag}' questions.
2. **'{slowest_tag}'** is slowest to first response ({s['frt_by_tag'].max():.1f}h median) —
   add a tag-triggered auto-reply and route to the most technical agent.
3. Staff the **{s['peak_hour']}:00** peak; move email backlog triage earlier in the day.
"""
    REPORT.write_text(report)
    print(f"Wrote {REPORT}")
    print(f"\nHeadline: {s['tickets']:,} tickets, {s['median_frt']:.1f}h median FRT, "
          f"{s['csat']:.2f}/5 CSAT. Worst tag: '{worst_tag}'. Slowest tag: '{slowest_tag}'.")


if __name__ == "__main__":
    main()
