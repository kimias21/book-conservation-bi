"""Project paths and analysis constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
INTEGRATED_CSV = DATA_PROCESSED / "integrated_heritage_books.csv"
ENV_MONITORING_CSV = DATA_RAW / "environmental_monitoring.csv"
VOLUMES_CSV = DATA_RAW / "volumes_metadata.csv"
SITES_CSV = DATA_RAW / "sites.csv"

# UNI 10829-inspired comfort bands (illustrative operational targets; see report)
RH_OPTIMAL_LOW = 45.0
RH_OPTIMAL_HIGH = 55.0
TEMP_OPTIMAL_LOW = 18.0
TEMP_OPTIMAL_HIGH = 22.0
LIGHT_MAX_LUX = 50.0

RANDOM_SEED = 42
