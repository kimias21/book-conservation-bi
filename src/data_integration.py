"""
Phase 1 — Dataset construction and integration.

Builds an integrated table linking heritage volumes, storage sites,
environmental monitoring, and derived conservation indicators.

Data provenance is documented in data/raw/DATA_PROVENANCE.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED,
    DATA_RAW,
    ENV_MONITORING_CSV,
    INTEGRATED_CSV,
    RANDOM_SEED,
    SITES_CSV,
    VOLUMES_CSV,
)
from src.conservation_index import add_conservation_columns

# Real European heritage institutions (coordinates approximate, public knowledge)
SITES = [
    {
        "site_id": "S01",
        "site_name": "Biblioteca Joanina, University of Coimbra",
        "site_type": "library",
        "country": "Portugal",
        "city": "Coimbra",
        "latitude": 40.2075,
        "longitude": -8.4266,
        "climate_zone": "Mediterranean",
        "collection_size_volumes": 250000,
    },
    {
        "site_id": "S02",
        "site_name": "Universitätsbibliothek Heidelberg",
        "site_type": "library",
        "country": "Germany",
        "city": "Heidelberg",
        "latitude": 49.4093,
        "longitude": 8.6944,
        "climate_zone": "Oceanic",
        "collection_size_volumes": 180000,
    },
    {
        "site_id": "S03",
        "site_name": "Biblioteca comunale dell'Archiginnasio",
        "site_type": "library",
        "country": "Italy",
        "city": "Bologna",
        "latitude": 44.4929,
        "longitude": 11.3430,
        "climate_zone": "Humid subtropical",
        "collection_size_volumes": 850000,
    },
    {
        "site_id": "S04",
        "site_name": "Archivio di Stato di Firenze",
        "site_type": "archive",
        "country": "Italy",
        "city": "Florence",
        "latitude": 43.7696,
        "longitude": 11.2558,
        "climate_zone": "Mediterranean",
        "collection_size_volumes": 1200000,
    },
    {
        "site_id": "S05",
        "site_name": "Bibliothèque nationale de France",
        "site_type": "library",
        "country": "France",
        "city": "Paris",
        "latitude": 48.8336,
        "longitude": 2.3758,
        "climate_zone": "Oceanic",
        "collection_size_volumes": 40000000,
    },
    {
        "site_id": "S06",
        "site_name": "British Library — St Pancras",
        "site_type": "library",
        "country": "United Kingdom",
        "city": "London",
        "latitude": 51.5300,
        "longitude": -0.1274,
        "climate_zone": "Oceanic",
        "collection_size_volumes": 170000000,
    },
    {
        "site_id": "S07",
        "site_name": "Marmottan Repository (simulated cold store)",
        "site_type": "repository",
        "country": "France",
        "city": "Paris",
        "latitude": 48.8606,
        "longitude": 2.2664,
        "climate_zone": "Oceanic",
        "collection_size_volumes": 45000,
    },
    {
        "site_id": "S08",
        "site_name": "Biblioteca Medicea Laurenziana",
        "site_type": "library",
        "country": "Italy",
        "city": "Florence",
        "latitude": 43.7743,
        "longitude": 11.2530,
        "climate_zone": "Mediterranean",
        "collection_size_volumes": 110000,
    },
]

SUPPORT_MATERIALS = ["parchment", "laid_paper", "industrial_paper", "mixed"]
INK_TYPES = ["iron_gall", "carbon", "printing_ink", "pigment"]
BINDING_TYPES = ["wood_boards", "leather", "vellum", "paper_boards", "none"]
COVER_TYPES = ["leather", "vellum", "paper", "wood", "none"]


def _rng() -> np.random.Generator:
    return np.random.default_rng(RANDOM_SEED)


def build_sites_df() -> pd.DataFrame:
    return pd.DataFrame(SITES)


def build_environmental_monitoring(sites_df: pd.DataFrame) -> pd.DataFrame:
    """
    Six-month monitoring campaign per site (monthly aggregates).

    Coimbra (S01) bands informed by published historic-library monitoring
    (Ferreira et al., Data in Brief, 2019 — RH ~40–70%, T seasonal variation).
    Other sites stochastically perturbed by climate_zone for integration demo.
    """
    rng = _rng()
    rows = []
    months = pd.date_range("2024-01-01", periods=6, freq="MS")

    zone_profiles = {
        "Mediterranean": {"temp_base": 19.5, "rh_base": 52, "light": 42},
        "Oceanic": {"temp_base": 18.0, "rh_base": 48, "light": 35},
        "Humid subtropical": {"temp_base": 20.0, "rh_base": 58, "light": 38},
    }

    for _, site in sites_df.iterrows():
        profile = zone_profiles.get(site["climate_zone"], zone_profiles["Oceanic"])
        # Coimbra: slightly wider RH per literature
        rh_spread = 12 if site["site_id"] == "S01" else 8
        for i, month in enumerate(months):
            seasonal = np.sin(2 * np.pi * i / 12) * 2.5
            temp = profile["temp_base"] + seasonal + rng.normal(0, 0.8)
            rh = profile["rh_base"] + seasonal * 1.5 + rng.normal(0, 3)
            if site["site_id"] == "S01":
                rh = np.clip(rh, 38, 68)
            light = max(5, profile["light"] + rng.normal(0, 6))
            aqi = int(np.clip(35 + rng.normal(15, 12), 20, 120))
            flood = site["site_type"] == "archive" and rng.random() < 0.04
            hvac = rng.random() < 0.06
            rows.append(
                {
                    "site_id": site["site_id"],
                    "month": month.strftime("%Y-%m"),
                    "avg_temperature_c": round(float(temp), 2),
                    "avg_relative_humidity_pct": round(float(rh), 2),
                    "avg_light_lux": round(float(light), 2),
                    "air_quality_index": aqi,
                    "flood_event": bool(flood),
                    "hvac_failure_event": bool(hvac),
                }
            )

    env = pd.DataFrame(rows)
    # Campaign-level aggregates for join to volumes
    agg = (
        env.groupby("site_id")
        .agg(
            avg_temperature_c=("avg_temperature_c", "mean"),
            avg_relative_humidity_pct=("avg_relative_humidity_pct", "mean"),
            avg_light_lux=("avg_light_lux", "mean"),
            air_quality_index=("air_quality_index", "mean"),
            flood_event=("flood_event", "max"),
            hvac_failure_event=("hvac_failure_event", "max"),
            monitoring_months=("month", "count"),
        )
        .reset_index()
    )
    agg["air_quality_index"] = agg["air_quality_index"].round(0).astype(int)
    return env, agg


def build_volumes_metadata(sites_df: pd.DataFrame, n_volumes: int = 480) -> pd.DataFrame:
    """
    Volume catalogue inspired by Europeana / national-library metadata fields.

    Records are procedurally generated but structurally aligned with
    open heritage catalogues (date, type, provider, place).
    """
    rng = _rng()
    site_ids = sites_df["site_id"].tolist()
    weights = np.array([0.12, 0.14, 0.16, 0.14, 0.12, 0.12, 0.08, 0.12])
    weights /= weights.sum()

    rows = []
    for i in range(n_volumes):
        site_id = rng.choice(site_ids, p=weights)
        century = int(rng.choice(range(12, 20), p=[0.08, 0.1, 0.12, 0.14, 0.16, 0.14, 0.12, 0.14]))
        if century <= 14:
            support = rng.choice(SUPPORT_MATERIALS, p=[0.45, 0.35, 0.05, 0.15])
            ink = rng.choice(INK_TYPES, p=[0.35, 0.35, 0.05, 0.25])
            binding = rng.choice(BINDING_TYPES, p=[0.3, 0.25, 0.25, 0.1, 0.1])
        elif century <= 17:
            support = rng.choice(SUPPORT_MATERIALS, p=[0.2, 0.5, 0.1, 0.2])
            ink = rng.choice(INK_TYPES, p=[0.4, 0.2, 0.15, 0.25])
            binding = rng.choice(BINDING_TYPES, p=[0.25, 0.3, 0.15, 0.2, 0.1])
        else:
            support = rng.choice(SUPPORT_MATERIALS, p=[0.05, 0.25, 0.55, 0.15])
            ink = rng.choice(INK_TYPES, p=[0.15, 0.1, 0.55, 0.2])
            binding = rng.choice(BINDING_TYPES, p=[0.1, 0.25, 0.1, 0.45, 0.1])

        restoration = rng.random() < 0.12
        condition_observed = int(
            np.clip(
                rng.normal(3.5 - (century - 12) * 0.08, 0.9) + (0.5 if restoration else -0.2),
                1,
                5,
            )
        )  # 1=poor, 5=excellent (expert survey proxy)

        rows.append(
            {
                "volume_id": f"V{i+1:04d}",
                "site_id": site_id,
                "title": f"Manuscript or printed volume {i+1:04d}",
                "century": century,
                "production_year_est": (century - 1) * 100 + int(rng.integers(0, 99)),
                "support_material": support,
                "ink_type": ink,
                "binding_type": binding,
                "cover_type": rng.choice(COVER_TYPES),
                "language": rng.choice(["Latin", "Italian", "French", "German", "English", "Greek"]),
                "format": rng.choice(["folio", "quarto", "octavo", "scroll"]),
                "restoration_recent": restoration,
                "observed_condition_score": condition_observed,
                "digitised": bool(rng.random() < 0.35),
                "source_catalogue": rng.choice(
                    ["Europeana", "Heidelberg UB", "ICCU", "BNF", "British Library"],
                ),
                "licence": "CC BY-SA 4.0 (metadata simulation)",
            }
        )
    return pd.DataFrame(rows)


def integrate(
    sites_df: pd.DataFrame,
    volumes_df: pd.DataFrame,
    env_agg: pd.DataFrame,
    env_monthly: pd.DataFrame,
) -> pd.DataFrame:
    df = volumes_df.merge(sites_df, on="site_id", how="left")
    df = df.merge(env_agg, on="site_id", how="left", suffixes=("", "_env"))
    return df


def export_data_dictionary(path: Path, df: pd.DataFrame) -> None:
    dictionary = {
        col: str(df[col].dtype) for col in df.columns
    }
    path.write_text(json.dumps(dictionary, indent=2), encoding="utf-8")


def run(n_volumes: int = 480) -> pd.DataFrame:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    sites_df = build_sites_df()
    env_monthly, env_agg = build_environmental_monitoring(sites_df)
    volumes_df = build_volumes_metadata(sites_df, n_volumes=n_volumes)

    sites_df.to_csv(SITES_CSV, index=False)
    env_monthly.to_csv(ENV_MONITORING_CSV, index=False)
    volumes_df.to_csv(VOLUMES_CSV, index=False)

    integrated = integrate(sites_df, volumes_df, env_agg, env_monthly)
    integrated = add_conservation_columns(integrated)
    integrated.to_csv(INTEGRATED_CSV, index=False)

    env_monthly.to_csv(DATA_PROCESSED / "environmental_timeseries.csv", index=False)
    export_data_dictionary(DATA_PROCESSED / "data_dictionary.json", integrated)

    print(f"Wrote {len(integrated)} records to {INTEGRATED_CSV}")
    return integrated


def main() -> None:
    parser = argparse.ArgumentParser(description="Build integrated heritage dataset")
    parser.add_argument("--volumes", type=int, default=480, help="Number of volumes")
    args = parser.parse_args()
    run(n_volumes=args.volumes)


if __name__ == "__main__":
    main()
