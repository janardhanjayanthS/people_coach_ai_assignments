# People Coach AI — Teams Bot

A Microsoft Teams bot that answers HR queries using the People Coach AI backend. Replies with an Adaptive Card including 👍 / 👎 feedback buttons.

## Prerequisites

- Python 3.12+
- Node.js + npm (for Teams App Test Tool)

## Setup

1. **Install dependencies**

   Using `uv` (recommended):

   ```bash
   uv sync
   ```

   Or with `pip`:

   ```bash
   pip install -r src/requirements.txt
   ```

2. **Configure environment**

   Create `src/.env`:

   ```
   PEOPLECOACH_AI_CHAT_ENDPOINT=<ask team for dev endpoint URL>
   ```

3. **Install Teams App Test Tool** (once)

   ```bash
   npm install -g @microsoft/teams-app-test-tool
   ```

## Running

**Terminal 1 — start the bot:**

```bash
cd src
python app.py
```

Bot runs on `http://localhost:3978`.

**Terminal 2 — start the test UI:**

```bash
teamsapptester start
```

Opens a browser with a Teams-like chat UI. Type any query to test.

## What it does

1. User sends a message → bot POSTs to `/chat` backend → replies with an Adaptive Card
2. Card shows the response text with 👍 / 👎 buttons
3. Clicking 👍 or 👎 opens a sub-card with a text input
4. Submitting feedback POSTs to `/message_feedback` backend

## Project structure

```
src/
├── app.py       # aiohttp server, bot adapter
├── bot.py       # message handler, feedback handler
├── card.py      # Adaptive Card builder
├── ai.py        # backend API calls (/chat, /message_feedback)
├── config.py    # app credentials (blank for local)
└── log.py       # logging setup
```
