"""
DealHunter AI - Configuration & Environment Setup
Handles API keys, dataset paths, and scoring constants.
"""

import os
from pathlib import Path
# Load local environment if dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent

# Dataset paths
DEFAULT_VENDORS_FILE = os.getenv("VENDORS_FILE", str(BASE_DIR / "vendors.json"))
EVIDENCE_DIR = BASE_DIR / "evidence"

# API keys and integrations
NEATLOGS_API_KEY = os.getenv("NEATLOGS_API_KEY", "")
NEATLOGS_PROJECT_ID = os.getenv("NEATLOGS_PROJECT_ID", "dealhunter-neathack-2026")
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/Meta-Llama-3.1-8B-Instruct")

# Default Evidence-Driven Scoring Weights (Section 4)
DEFAULT_WEIGHTS = {
    "tco": 0.35,          # Total cost of ownership: 35%
    "features": 0.25,     # Feature compatibility: 25%
    "evidence": 0.20,     # Evidence quality: 20%
    "reliability": 0.15,  # Reliability and support: 15%
    "flexibility": 0.05,  # Contract flexibility: 5%
}

# Retry Policy limits
MAX_RETRY_ATTEMPTS = 3
INITIAL_BACKOFF_SECONDS = 0.5
TIMEOUT_SECONDS = 5.0

# Ensure evidence dir exists
os.makedirs(EVIDENCE_DIR, exist_ok=True)
