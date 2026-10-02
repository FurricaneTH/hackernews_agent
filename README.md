# Hacker News Morning Agent

A lightweight Python agent that scans Hacker News, prioritizes AI and technology stories, reads the original articles, and produces concise Turkish summaries with the OpenAI Responses API.

The project is designed to be easy to run manually today and easy to connect to a website or scheduled workflow later.

## What it does

```text
Hacker News top stories
          ↓
Scan the first 30 stories
          ↓
Prioritize AI-related titles
          ↓
Select up to 5 stories
          ↓
Read the original articles
          ↓
Summarize them in Turkish with GPT-5.6 Luna
          ↓
Print to the terminal or send by email
```

The title filter runs locally in Python, so scanning and prioritizing stories does not require an additional OpenAI request. Only the selected article content is sent for summarization.

## Story prioritization

The agent scans the first 30 entries in Hacker News' current `topstories` feed. It assigns higher scores to AI-focused terms such as:

- AI and artificial intelligence
- LLM and large language model
- RAG and genAI
- GPT, OpenAI, Anthropic, Claude, and Gemini
- machine learning and deep learning
- transformers, embeddings, inference, and AI agents

General technology terms such as software, programming, Linux, databases, cloud, hardware, cybersecurity, and APIs receive a lower priority. The agent selects up to 5 matching stories, keeping the original Hacker News order when scores are equal.

## Summary format

For each selected article, the agent asks the model to produce a compact Turkish summary with:

1. A 3–4 sentence overview
2. Up to 4 key points
3. Why the article matters
4. Up to 3 brief explanations of technical terms when needed

The summarizer is instructed to use only the supplied article text and not invent information.

## Requirements

- Python 3.10 or newer
- An OpenAI API key with available API credit
- A Gmail account and Google App Password only if email delivery is enabled

## Installation

```bash
git clone https://github.com/FurricaneTH/hackernews_agent.git
cd hackernews-morning-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Then fill in the values locally:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.6-luna
OPENAI_REASONING_EFFORT=minimal
MAX_OUTPUT_TOKENS=1200

SCAN_COUNT=30
MAX_SUMMARIES=5

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail_address
SMTP_PASSWORD=your_google_app_password
EMAIL_FROM=your_gmail_address
EMAIL_TO=recipient@example.com
```

`SMTP_PASSWORD` must be a Google App Password, not your normal Gmail password. Google requires 2-Step Verification before an App Password can be created.

The `.env` file is ignored by Git and must never be committed. The repository only contains `.env.example` as a configuration template.

## Usage

### Preview selected stories

This scans Hacker News and displays the selected titles and links. It does not read articles, call OpenAI, or send email.

```bash
python main.py --preview
```

### Generate summaries without sending email

This reads the selected articles, summarizes them with the configured model, and prints the results to the terminal.

```bash
python main.py --no-email
```

### Generate summaries and send an email

This runs the complete current CLI flow and sends the digest using SMTP.

```bash
python main.py
```

### List the most recent API usage and charges

Every summarization call appends its token usage and estimated cost to `usage_log.jsonl`. This command lists the latest records, newest first:

```bash
python main.py --usage
python main.py --usage --usage-limit 25   # 0 lists every record
```

Estimated costs are only printed when the per-million-token prices are configured in `.env`:

```dotenv
OPENAI_INPUT_PRICE_PER_1M=1.25
OPENAI_OUTPUT_PRICE_PER_1M=10
USAGE_LOG_PATH=
```

A normal run also prints the total tokens and estimated cost of that run. The log file contains no credentials, but it is ignored by Git by default.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Coordinates fetching, filtering, reading, summarization, and output |
| `hackernews.py` | Retrieves stories from the official Hacker News Firebase API |
| `filtering.py` | Scores and selects AI-focused and technology stories locally |
| `article_reader.py` | Downloads article pages and extracts readable text |
| `summarizer.py` | Calls the OpenAI Responses API and creates Turkish summaries |
| `email_sender.py` | Sends the digest through Gmail SMTP |
| `usage_log.py` | Records token usage and estimated cost per API call and lists recent records |
| `.env.example` | Safe configuration template without secrets |
| `requirements.txt` | Python dependencies |

## Cost considerations

Hacker News API requests, local title filtering, article downloads, and Gmail SMTP delivery do not use OpenAI credits. OpenAI usage is generated only when the selected article text is sent to the summarization model.

The number of stories scanned does not directly determine the OpenAI cost. For example, scanning 20 or 30 titles costs the same on the OpenAI side if both configurations summarize 5 articles. Increasing `MAX_SUMMARIES`, article length, output length, or run frequency increases usage.

Actual usage is tracked locally: each call stores its input, output, and total tokens in `usage_log.jsonl`, and `python main.py --usage` lists the most recent charges with their estimated cost.

The model is configurable through `OPENAI_MODEL`. The current default is `gpt-5.6-luna`, selected for the quality and cost balance required by this workflow.

## Security notes

- Never share an OpenAI API key in chat, screenshots, or GitHub.
- Never commit `.env`, `.env.save`, or any other file containing credentials.
- Revoke and replace a key immediately if it is exposed.
- Keep OpenAI and SMTP credentials server-side when integrating this agent with a website.
- Use a Google App Password for SMTP instead of a normal Gmail password.

## Current status

- Hacker News API integration: complete
- Original article extraction: complete
- AI-focused title prioritization: complete
- Turkish article summarization: complete
- Terminal preview and no-email modes: complete
- Gmail SMTP delivery: implemented and tested
- API usage and cost logging: complete
- Site/database integration: handled by the separate website project
- Daily 09:00 scheduling: planned for a future deployment step

## Future improvements

- Store the latest summaries in a database such as Supabase
- Expose a secure server-side endpoint for website-triggered runs
- Keep only the latest 10 stories
- Add scheduled execution
- Add retry handling and per-article error reporting
- Add tests for filtering and article extraction

## License

This is a personal project. Add a license before distributing or reusing the code publicly.
