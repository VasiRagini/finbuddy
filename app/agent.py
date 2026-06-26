# ruff: noqa
# FinBuddy - Autonomous Financial Subscription Management Agent
# Built for Google/Kaggle 5-Day AI Agents Intensive Capstone

import json
import os
from datetime import datetime

from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# Load .env so GOOGLE_API_KEY is available
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ---------- TOOLS ----------

def read_transactions(filepath: str = "") -> str:
    """Reads mock transaction data from a JSON file.

    Args:
        filepath: Optional path override. Defaults to the bundled sample data.

    Returns:
        A JSON string of the transaction list.
    """
    if not filepath:
        filepath = str(Path(__file__).resolve().parent / "app_utils" / "sample_transactions.json")
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return json.dumps(data)
    except FileNotFoundError:
        return json.dumps({"error": f"File not found: {filepath}"})


def flag_anomalies(transactions_json: str) -> str:
    """Analyzes transactions and flags recurring subscriptions with anomalies
    such as price increases, duplicate charges, or long-unused services.

    Args:
        transactions_json: JSON string of transaction records.

    Returns:
        A JSON string listing flagged items with reason and severity.
    """
    try:
        transactions = json.loads(transactions_json)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid transaction JSON"})

    merchants = {}
    for tx in transactions:
        name = tx.get("merchant")
        merchants.setdefault(name, []).append(tx)

    flagged = []
    for name, txs in merchants.items():
        txs_sorted = sorted(txs, key=lambda t: t["date"])
        amounts = [t["amount"] for t in txs_sorted]

        if len(txs_sorted) >= 2 and amounts[-1] > amounts[0] * 1.15:
            flagged.append({
                "merchant": name,
                "reason": "price_increase",
                "old_amount": amounts[0],
                "new_amount": amounts[-1],
                "severity": "medium",
            })

        dates = [t["date"] for t in txs_sorted]
        if len(dates) != len(set(dates)):
            flagged.append({
                "merchant": name,
                "reason": "duplicate_charge",
                "severity": "high",
            })

        last_used = txs_sorted[-1].get("last_used_days_ago", 0)
        if last_used and last_used > 60:
            flagged.append({
                "merchant": name,
                "reason": "unused_subscription",
                "days_unused": last_used,
                "monthly_cost": amounts[-1],
                "severity": "low",
            })

    return json.dumps({"flagged_items": flagged})


def draft_action_message(merchant: str, reason: str, monthly_cost: float = 0) -> str:
    """Drafts a cancellation or negotiation message for a flagged subscription.

    Args:
        merchant: The name of the merchant/service.
        reason: Why it was flagged (e.g. price_increase, unused_subscription).
        monthly_cost: The current monthly cost of the subscription.

    Returns:
        A drafted message ready for the user to review and send.
    """
    if reason == "unused_subscription":
        strategy = "cancellation"
        message = (
            f"Hello {merchant} team,\n\nI'd like to cancel my subscription "
            f"effective immediately, as I have not been using the service. "
            f"Please confirm the cancellation and stop any future billing.\n\nThank you."
        )
    elif reason == "price_increase":
        strategy = "negotiation"
        message = (
            f"Hello {merchant} team,\n\nI noticed my subscription price has increased. "
            f"As a long-time customer, I'd like to ask if there's a loyalty discount "
            f"or retention offer available. If not, I may need to reconsider my subscription.\n\nThank you."
        )
    else:
        strategy = "review"
        message = (
            f"Hello {merchant} team,\n\nI noticed an unusual charge on my account "
            f"({reason}). Could you please clarify this charge?\n\nThank you."
        )

    return json.dumps({"merchant": merchant, "strategy": strategy, "draft_message": message})


# ---------- AGENTS ----------

transaction_analyst = Agent(
    name="transaction_analyst",
    model=Gemini(model=MODEL_NAME, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are the Transaction Analyst. Read transaction data using read_transactions, "
        "then call flag_anomalies on the result. Report the flagged items clearly, "
        "explaining each anomaly's reason and severity in plain language."
    ),
    tools=[read_transactions, flag_anomalies],
)

action_agent = Agent(
    name="action_agent",
    model=Gemini(model=MODEL_NAME, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are the Negotiation/Action Agent. For each flagged subscription "
        "from the previous step, call draft_action_message to create a cancellation "
        "or negotiation message. Present each drafted message clearly so the user "
        "can review before sending. Never claim to have actually sent anything."
    ),
    tools=[draft_action_message],
)

root_agent = SequentialAgent(
    name="finbuddy_orchestrator",
    sub_agents=[transaction_analyst, action_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)