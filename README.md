# GradPilots — UAE Education Intelligence Scraper

## Overview
This repository contains a **production-oriented web scraping pipeline** designed to collect, normalize, and structure authoritative university and education data for the **United Arab Emirates (UAE)**.

The system supports:
- Student counselling workflows
- Accreditation verification
- Analytics & recommendation engines
- Future API and database integration

The dataset is structured using a strict **three-layer data model**:

**Country → University → Course**

This mirrors real-world education intelligence systems and ensures long-term extensibility.

---

## Data Sources
The scraper consumes **only publicly available, authoritative sources**:

| Source | Purpose |
|------|--------|
| UAE CAA (Government) | Official accreditation & licensure status |
| BachelorsPortal | University & course discovery |
| UniversityLiving | Cost-of-living reference for students |

Each record includes **explicit source traceability** to avoid data ambiguity.

---

## Architecture & Design Decisions

### Hybrid Scraping Strategy
- **Static scraping (Requests + BeautifulSoup)** for government and editorial sources  
- **Dynamic scraping (Selenium)** for JavaScript-rendered portals  

This minimizes browser automation while remaining resilient to real-world websites.

---

### Data Integrity & Safety
- Accreditation status preserved exactly as published by the CAA  
- Revoked or inactive institutions explicitly labeled  
- No inferred or fabricated data  
- Empty datasets preferred over unsafe assumptions  

---

### Normalization & Search Readiness
- Deterministic `normalized_name` for every institution  
- Explicit institution typing (University, College, Institute, School, Academy)  
- Designed for filtering, joins, and indexing  

---

### Confidence & Traceability
Every institution includes:
- `data_confidence` level  
- Human-readable `confidence_reason`  
- `source_trace` indicating origin presence  

This is critical for **advisory and compliance-sensitive use cases**.

---

## Output Format
The primary output is an analytics-ready JSON file:

data/uae_education_data.json


It contains:
- Metadata (generation time, sources, update cadence)
- Country-level cost-of-living context
- Normalized university records
- Course placeholders ready for enrichment

The structure is **API-ready and database-friendly**.

---

## Project Structure
GradPilots_Scraper/
│
├── main.py
├── scrapers/
│ ├── portal_scraper.py
│ ├── caa_scraper.py
│ └── living_scraper.py
│
├── data/
│ └── uae_education_data.json
│
├── requirements.txt
├── Dockerfile
└── README.md


---

## Run Instructions

### Local Execution
```bash
pip install -r requirements.txt
python main.py
Docker (Optional)
bash
Copy code
docker build -t gradpilots-scraper .
docker run gradpilots-scraper

## Known Limitations
Course portal DOM selectors may evolve (React-based UI)

Cost-of-living data reflects Dubai only (explicitly scoped)

University name matching uses deterministic heuristics, not ML models

These are intentional MVP tradeoffs and are documented for future iteration.

## Extensibility Roadmap (Not Implemented by Design)
Course-level enrichment (fees, intakes, eligibility)

Multi-city cost-of-living normalization

API layer for real-time querying

Scheduled refresh pipelines (Cron / Airflow)

The current version prioritizes correctness, traceability, and safety over feature breadth.

## License & Usage
This project is intended for educational and internal analytics use.

All data is sourced from publicly accessible websites and remains subject to their respective terms.