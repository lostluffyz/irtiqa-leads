# Irtiqa AI

AI-powered lead intelligence and qualification infrastructure built with Python, Streamlit, Ollama, Playwright, and SQLite.

---

## Overview

Irtiqa AI is a multi-agent lead intelligence system designed to scrape, analyze, qualify, score, and visualize high-value business leads.

The system focuses on identifying:
- ICP-aligned businesses
- Operational pain points
- Lead quality
- Outreach opportunities
- Revenue bottlenecks

Current architecture follows a modular pipeline:

```text
SCRAPE → ANALYZE → SCORE → VISUALIZE
```

---

# Features

## Dashboard
- Modern dark-mode Streamlit dashboard
- KPI analytics cards
- Lead tier distribution
- Industry analytics
- Lead detail viewer
- Dynamic filters
- Search functionality
- CSV export
- Real-time database integration

## AI Lead Intelligence
- AI lead scoring
- Confidence scoring
- Pain point extraction
- Lead tiering
- Outreach generation
- Industry classification

## Infrastructure
- SQLite persistence
- Multi-agent architecture
- Modular pipeline design
- Dynamic analytics
- Scalable project structure

---

# Architecture

## Agent 1 — Scraper
Responsible for:
- Website scraping
- Raw lead collection
- Data extraction
- Pipeline ingestion

### Planned Expansion
- LinkedIn scraping
- Google Maps scraping
- Reddit/Twitter/GitHub/Crunchbase scraping
- Scheduling automation

---

## Agent 2 — Researcher / Verificator
Responsible for:
- Industry classification
- Lead verification
- Confidence scoring
- Pain point analysis

### Planned Expansion
- SMTP verification
- MX/DNS checks
- WHOIS verification
- Company size verification

---

## Agent 3 — Scorer
Responsible for:
- Lead scoring
- Tier assignment
- Pain point mapping
- Outreach preparation
- Dashboard visualization

### Planned Expansion
- Advanced weighted scoring
- Objection prediction
- AI reasoning improvements
- Multi-channel outreach

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Visualization | Plotly |
| AI/LLM | Ollama + Llama |
| Scraping | Playwright |

---

# Current System Progress

| System | Progress |
|---|---|
| Database Infrastructure | 90% |
| Dashboard & Visualization | 90% |
| Basic Scraping Pipeline | 55% |
| AI Classification | 45% |
| Verification Engine | 20% |
| Multi-Source Intelligence | 15% |
| Outreach Automation | 10% |
| Full Architecture Completion | 45% |

---

# Dashboard Preview

## Main Dashboard
(Add screenshot here)

## Lead Intelligence Panel
(Add screenshot here)

## Analytics View
(Add screenshot here)

---

# Recommended Development Order

## Phase 1 — Stabilize Architecture
- Fix remaining bugs
- Clean schema
- Refactor configs

## Phase 2 — Real AI Integration
- Ollama integration
- JSON classification
- Keyword extraction
- Pain point reasoning

## Phase 3 — Verification Engine
- SMTP checks
- Phone validation
- MX lookup
- SSL/domain analysis

## Phase 4 — Multi-Source Scraping
- LinkedIn
- Reddit
- Google Maps
- GitHub
- Crunchbase

## Phase 5 — Outreach Automation
- Follow-up sequences
- Booking pipeline
- CRM automation

## Phase 6 — Deploy & Scale
- Cloud deployment
- SaaS architecture
- Monitoring & analytics

---

# Installation

```bash
git clone https://github.com/lostluffyz/irtiqa-leads.git

cd irtiqa-leads

pip install -r requirements.txt

streamlit run dashboard/app.py
```

---

# Vision

Irtiqa AI aims to become a full autonomous lead intelligence infrastructure capable of:

- Scraping businesses
- Verifying legitimacy
- Detecting operational pain points
- Scoring lead quality
- Generating outreach
- Automating revenue workflows

---

# Project Status

This project is currently under active development.

The dashboard layer and database infrastructure are mostly complete, while AI enrichment, verification systems, and outreach automation are actively being expanded.

---

# License

Private/Internal Project