# Irtiqa AI

AI-powered lead generation and qualification system built with Python, Ollama, Playwright, and SQLite.

## Features

- Multi-agent architecture
- Lead scraping
- Email verification
- AI-based lead scoring
- Local LLM support with Ollama
- Streamlit dashboard
- CSV export pipeline

## Architecture

### Agent 1 — Scraper Agent
Collects raw lead data from:
- Google
- LinkedIn
- Reddit
- GitHub
- Company websites

### Agent 2 — Researcher Agent
Verifies and enriches leads:
- Email validation
- Phone validation
- Industry classification
- Pain point detection

### Agent 3 — Scorer Agent
Scores and qualifies leads:
- ICP matching
- Outreach generation
- AI-powered qualification

## Tech Stack

- Python
- Playwright
- BeautifulSoup4
- SQLite
- Ollama
- Streamlit
- Pandas
- httpx

## Status

Under active development.