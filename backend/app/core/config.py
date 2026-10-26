"""Repository-aware paths; no dependence on process working directory."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = Path(os.getenv("BR_MODEL_DIR", ROOT / "models"))
EXPORT_DIR = Path(os.getenv("BR_EXPORT_DIR", ROOT / "exports"))
MAX_ITEMS = 20
MAX_RESULTS = 20
