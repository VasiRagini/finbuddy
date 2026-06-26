\# FinBuddy: Your Autonomous Subscription Watchdog



\## The Problem



Most people have 5-15 recurring subscriptions — streaming, fitness apps, cloud storage, software tools. Prices creep up quietly. Subscriptions get forgotten. Duplicate charges slip through unnoticed. Nobody has time to audit their bank statement every month, and by the time they notice, they've often lost hundreds of dollars.



\## The Solution



FinBuddy is a multi-agent system that doesn't just \*report\* subscription problems — it \*acts\* on them. Given transaction data, it:



1\. Detects price increases, unused subscriptions, and duplicate charges

2\. Drafts a ready-to-send message for each issue — a negotiation request, a cancellation notice, or a billing inquiry — tailored to the specific problem

3\. Presents everything for the user's review before anything is "sent" (human-in-the-loop by design — FinBuddy never claims to act autonomously without consent)



\## Architecture



FinBuddy uses a \*\*SequentialAgent orchestrator\*\* coordinating two specialized sub-agents, built on Google ADK:



\- \*\*Transaction Analyst\*\* — reads transaction data and flags anomalies using two custom tools (`read\_transactions`, `flag\_anomalies`)

\- \*\*Action Agent\*\* — drafts an appropriate response for each flagged item using `draft\_action\_message`, choosing strategy (negotiate vs. cancel vs. inquire) based on the anomaly type



This is a genuine multi-agent pipeline, not a single chatbot with branching logic — each agent has its own instruction, its own tools, and a distinct role in the pipeline.



\## Course Concepts Applied



\- \*\*Tool Use (Day 2):\*\* Three custom Python tools wired into ADK agents, each with typed signatures and docstrings

\- \*\*Multi-Agent Orchestration (Day 5):\*\* `SequentialAgent` coordinating two `LlmAgent` sub-agents with clear separation of concerns

\- \*\*Stateful Reasoning (Day 3):\*\* The pipeline carries context from raw transactions → flagged anomalies → drafted actions, with each stage building on the last



\## Why This Matters



Subscription overspending is a quiet, universal financial drain. FinBuddy turns a tedious, easy-to-postpone task (auditing your subscriptions) into a single command, with concrete, actionable output — not just insight, but a drafted next step.



\## Demo



Video: https://youtu.be/Vl3WDbFmp50

GitHub: https://github.com/VasiRagini/finbuddy



\## Tech Stack



Google ADK, Gemini 2.5 Flash, Python — built and tested entirely locally.

