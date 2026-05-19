"""Conservation Risk Index (CRI) — synthetic indicator for decision support."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import (
    LIGHT_MAX_LUX,
    RH_OPTIMAL_HIGH,
    RH_OPTIMAL_LOW,
    TEMP_OPTIMAL_HIGH,
    TEMP_OPTIMAL_LOW,
)

# Material vulnerability (higher = more sensitive); motivated in report §3.3
MATERIAL_VULNERABILITY = {
    "parchment": 1.0,
    "laid_paper": 0.75,
    "industrial_paper": 0.45,
    "mixed": 0.85,
}

INK_VULNERABILITY = {
    "iron_gall": 0.9,
    "carbon": 0.5,
    "printing_ink": 0.4,
    "pigment": 0.6,
}

BINDING_VULNERABILITY = {
    "wood_boards": 0.85,
    "leather": 0.7,
    "vellum": 0.8,
    "paper_boards": 0.55,
    "none": 0.4,
}


def _band_stress(value: float, low: float, high: float, scale: float = 10.0) -> float:
    """Distance outside optimal band, capped at 1."""
    if low <= value <= high:
        return 0.0
    if value < low:
        dist = low - value
    else:
        dist = value - high
    return min(1.0, dist / scale)


def environmental_stress(row: pd.Series) -> float:
    rh = _band_stress(row["avg_relative_humidity_pct"], RH_OPTIMAL_LOW, RH_OPTIMAL_HIGH, 15.0)
    temp = _band_stress(row["avg_temperature_c"], TEMP_OPTIMAL_LOW, TEMP_OPTIMAL_HIGH, 8.0)
    light = min(1.0, max(0.0, (row["avg_light_lux"] - LIGHT_MAX_LUX) / 80.0))
    aqi = min(1.0, max(0.0, (row["air_quality_index"] - 50) / 100.0))
    return float(np.clip(0.4 * rh + 0.3 * temp + 0.2 * light + 0.1 * aqi, 0, 1))


def material_stress(row: pd.Series) -> float:
    mat = MATERIAL_VULNERABILITY.get(row["support_material"], 0.7)
    ink = INK_VULNERABILITY.get(row["ink_type"], 0.6)
    binding = BINDING_VULNERABILITY.get(row["binding_type"], 0.6)
    return float(np.clip(0.5 * mat + 0.25 * ink + 0.25 * binding, 0, 1))


def age_stress(century: int, reference_year: int = 2025) -> float:
    """Older volumes assumed higher baseline deterioration potential."""
    if century <= 0:
        return 0.5
    mid_year = (century - 1) * 100 + 50
    years = max(0, reference_year - mid_year)
    return float(np.clip(years / 800.0, 0.1, 1.0))


def event_stress(row: pd.Series) -> float:
    score = 0.0
    if row.get("flood_event", False):
        score += 0.5
    if row.get("restoration_recent", False):
        score += 0.15
    if row.get("hvac_failure_event", False):
        score += 0.25
    return min(1.0, score)


def compute_cri(row: pd.Series) -> float:
    """
    Conservation Risk Index on scale 0–100 (higher = worse).
    Weights chosen for interpretability; sensitivity analysis in notebook.
    """
    env = environmental_stress(row)
    mat = material_stress(row)
    age = age_stress(int(row["century"]))
    events = event_stress(row)
    composite = 0.35 * env + 0.30 * mat + 0.25 * age + 0.10 * events
    return round(float(composite * 100), 2)


def risk_label(cri: float) -> str:
    if cri < 35:
        return "Low"
    if cri < 55:
        return "Moderate"
    if cri < 75:
        return "High"
    return "Critical"


def add_conservation_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    drop_cols = [
        "environmental_stress",
        "material_stress",
        "age_stress",
        "event_stress",
        "conservation_risk_index",
        "risk_level",
        "high_risk",
    ]
    out = out.drop(columns=[c for c in drop_cols if c in out.columns])
    out["environmental_stress"] = out.apply(environmental_stress, axis=1)
    out["material_stress"] = out.apply(material_stress, axis=1)
    out["age_stress"] = out["century"].apply(age_stress)
    out["event_stress"] = out.apply(event_stress, axis=1)
    out["conservation_risk_index"] = out.apply(compute_cri, axis=1)
    out["risk_level"] = out["conservation_risk_index"].apply(risk_label)
    out["high_risk"] = (out["conservation_risk_index"] >= 55).astype(int)
    return out
