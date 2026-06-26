# FinBuddy 💰🤖

**Autonomous Financial Subscription Management Agent**
Built for the Google/Kaggle 5-Day AI Agents Intensive — Capstone Project

## What FinBuddy Does

FinBuddy is a multi-agent system that monitors your recurring subscriptions and *takes action* on what it finds — not just reporting problems, but drafting ready-to-send messages to resolve them.

It detects three kinds of issues:
- **Price increases** on existing subscriptions
- **Unused subscriptions** still being billed
- **Duplicate charges** from the same merchant

For each issue, it drafts an appropriate response — a negotiation message, a cancellation request, or a billing inquiry — tailored to the situation.

## Architecture
finbuddy_orchestrator (SequentialAgent)
├── transaction_analyst (LlmAgent)
│   ├── read_transactions()   → loads transaction data
│   └── flag_anomalies()      → detects price hikes, duplicates, unused subs
└── action_agent (LlmAgent)
└── draft_action_message() → drafts cancellation/negotiation/inquiry messages
This maps directly to course concepts from the 5-Day AI Agents Intensive:
- **Day 2 (Tools & Interoperability):** Custom Python tools wired into ADK agents
- **Day 3 (Agent Skills):** Stateful reasoning across the transaction → flag → action pipeline
- **Day 5 (Production Development):** Multi-agent orchestration via `SequentialAgent`

## Project Structure
finbuddy/
├── app/
│   ├── agent.py                    # Core agent logic (3 agents + 3 tools)
│   ├── agent_runtime_app.py        # Agent Runtime application logic
│   └── app_utils/
│       └── sample_transactions.json  # Mock transaction data
├── tests/                          # Unit, integration, and load tests
├── .env                            # API config (not committed)
└── pyproject.toml                  # Project dependencies
## Setup & Run

1. **Install dependencies:**
   ```bash
   uv sync
2.Configure your API key — create a .env file in this folder:
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=False
GEMINI_MODEL=gemini-2.5-flash
Get a free key at Google AI Studio.
3.Run the local playground:
uv run adk web app --host 127.0.0.1 --port 18081
4.Open http://127.0.0.1:18081 and try:
Check my subscriptions for any issues
Sample Output
Given the bundled mock data (Netflix, Spotify, GymFitPro, CloudStorageX), FinBuddy correctly identifies:
Netflix → price increase (199 → 249) → drafts a negotiation message
GymFitPro → unused for 95 days → drafts a cancellation message
CloudStorageX → duplicate charge → drafts a billing inquiry
Spotify (no issues) is correctly left unflagged.
Tech Stack
Google ADK (Agent Development Kit) — multi-agent orchestration
Gemini 2.5 Flash — underlying LLM
Python — tool implementations
Built and tested locally, no cloud deployment required
Built By
Ragini — B.Tech AI & ML, SVCE Tirupati
GitHub | LinkedIn
