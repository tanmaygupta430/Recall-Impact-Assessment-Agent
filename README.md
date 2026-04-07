# Recall-Impact-Assessment-Agent
This is an LLM agent that identifies hospital inventories affected by an FDA product recall. The agent identifies the products at the hospital using a Cortex search and creates an executive summary to be shared with the hospital, along with the dollar value at risk if the product is not returned

# 🏥 FDA Recall Impact Assessment Agent
### Built with Snowflake Cortex AI | Healthcare Supply Chain

## The Problem
When the FDA issues a medical device or drug recall, the hospital supply chain teams manually cross-reference inventory, identify affected departments, and draft stakeholder alerts — a process that takes 2-3 days, and is prone to error.

## The Solution
An AI agent that ingests an FDA recall notice, cross-references it against hospital inventory in real time, quantifies financial exposure, and drafts an internal alert — in under 60 seconds.

## Architecture
FDA OpenFDA API → Snowflake Table → Cortex Search → Cortex Complete → Streamlit UI

## Features
- Real-time FDA recall ingestion via OpenFDA API
- Natural language inventory matching using Cortex Search
- Financial exposure quantification by department
- Auto-generated stakeholder alert draft
- Interactive Streamlit dashboard

## Tech Stack
- Snowflake Cortex (Search + Complete)
- Streamlit in Snowflake
- Python + Snowpark
- OpenFDA Public API

## How to Run
1. Clone this repo
2. Set up Snowflake credentials in `.env.`
3. Run `setup.sql` in your Snowflake account
4. Deploy `app.py` as a Streamlit in Snowflake app

## Data Sources
- FDA OpenFDA Device Recall API (public)
- Simulated hospital inventory (representative of real supply data)

## Portfolio Context
Built as part of a Healthcare Supply Chain AI portfolio to demonstrate product thinking + technical execution.
