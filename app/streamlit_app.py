"""
Phase 3 — Streamlit BI dashboard for conservation state analysis.
Run: streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.conservation_index import compute_cri, risk_label
from src.config import DATA_PROCESSED, INTEGRATED_CSV

st.set_page_config(
    page_title="Heritage Conservation BI",
    page_icon="📚",
    layout="wide",
)

MATERIAL_LABELS = {
    "parchment": "Parchment",
    "laid_paper": "Laid paper",
    "industrial_paper": "Industrial paper",
    "mixed": "Mixed support",
}


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not INTEGRATED_CSV.exists():
        st.error("Integrated dataset not found. Run: `python -m src.data_integration`")
        st.stop()
    books = pd.read_csv(INTEGRATED_CSV)
    ts_path = DATA_PROCESSED / "environmental_timeseries.csv"
    timeseries = pd.read_csv(ts_path) if ts_path.exists() else pd.DataFrame()
    return books, timeseries


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    centuries = st.session_state.get("f_centuries", [])
    if centuries:
        out = out[out["century"].isin(centuries)]
    materials = st.session_state.get("f_materials", [])
    if materials:
        out = out[out["support_material"].isin(materials)]
    countries = st.session_state.get("f_countries", [])
    if countries:
        out = out[out["country"].isin(countries)]
    site_types = st.session_state.get("f_site_types", [])
    if site_types:
        out = out[out["site_type"].isin(site_types)]
    rh = st.session_state.get("f_rh", (30.0, 70.0))
    out = out[
        (out["avg_relative_humidity_pct"] >= rh[0])
        & (out["avg_relative_humidity_pct"] <= rh[1])
    ]
    temp = st.session_state.get("f_temp", (15.0, 25.0))
    out = out[
        (out["avg_temperature_c"] >= temp[0])
        & (out["avg_temperature_c"] <= temp[1])
    ]
    return out


def sidebar_filters(df: pd.DataFrame) -> None:
    st.sidebar.header("Filters")
    st.session_state["f_centuries"] = st.sidebar.multiselect(
        "Century",
        sorted(df["century"].unique()),
        default=sorted(df["century"].unique()),
    )
    st.session_state["f_materials"] = st.sidebar.multiselect(
        "Support material",
        options=sorted(df["support_material"].unique()),
        format_func=lambda x: MATERIAL_LABELS.get(x, x),
        default=sorted(df["support_material"].unique()),
    )
    st.session_state["f_countries"] = st.sidebar.multiselect(
        "Country",
        sorted(df["country"].unique()),
        default=sorted(df["country"].unique()),
    )
    st.session_state["f_site_types"] = st.sidebar.multiselect(
        "Site type",
        sorted(df["site_type"].unique()),
        default=sorted(df["site_type"].unique()),
    )
    st.session_state["f_rh"] = st.sidebar.slider(
        "Relative humidity range (%)",
        30.0,
        70.0,
        (float(df["avg_relative_humidity_pct"].min()), float(df["avg_relative_humidity_pct"].max())),
    )
    st.session_state["f_temp"] = st.sidebar.slider(
        "Temperature range (°C)",
        15.0,
        25.0,
        (float(df["avg_temperature_c"].min()), float(df["avg_temperature_c"].max())),
    )


def kpi_row(df: pd.DataFrame) -> None:
    n = len(df)
    high = (df["conservation_risk_index"] >= 55).sum()
    critical = (df["conservation_risk_index"] >= 75).sum()
    mean_cri = df["conservation_risk_index"].mean()
    sites_at_risk = df.groupby("site_id")["conservation_risk_index"].mean()
    n_sites = (sites_at_risk >= 55).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Volumes analysed", f"{n:,}")
    c2.metric("Mean CRI", f"{mean_cri:.1f}")
    c3.metric("High/Critical risk", f"{high:,} ({100*high/max(n,1):.1f}%)")
    c4.metric("Critical only", f"{critical:,}")
    c5.metric("Sites above mean risk", f"{n_sites}")


def main_dashboard(df: pd.DataFrame, timeseries: pd.DataFrame) -> None:
    st.title("Conservation state of ancient books")
    st.caption(
        "Business Intelligence dashboard for curators and conservators — "
        "IS & BI course project A.Y. 2025/2026"
    )
    kpi_row(df)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Geography & time", "Drill-down", "What-if & priorities"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_risk = px.histogram(
                df,
                x="conservation_risk_index",
                color="risk_level",
                nbins=25,
                title="Distribution of Conservation Risk Index",
                labels={"conservation_risk_index": "CRI (0–100)"},
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        with col2:
            by_mat = (
                df.groupby("support_material")["conservation_risk_index"]
                .mean()
                .reset_index()
            )
            by_mat["label"] = by_mat["support_material"].map(
                lambda m: MATERIAL_LABELS.get(m, m)
            )
            fig_mat = px.bar(
                by_mat,
                x="label",
                y="conservation_risk_index",
                title="Mean CRI by support material",
                labels={"conservation_risk_index": "Mean CRI"},
            )
            st.plotly_chart(fig_mat, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig_cent = px.box(
                df,
                x="century",
                y="conservation_risk_index",
                title="CRI by century of production",
            )
            st.plotly_chart(fig_cent, use_container_width=True)
        with col4:
            corr_cols = [
                "conservation_risk_index",
                "avg_relative_humidity_pct",
                "avg_temperature_c",
                "avg_light_lux",
                "age_stress",
                "material_stress",
            ]
            corr = df[corr_cols].corr()
            fig_corr = px.imshow(
                corr,
                text_auto=".2f",
                title="Correlation matrix (selected variables)",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
            )
            st.plotly_chart(fig_corr, use_container_width=True)

    with tab2:
        site_agg = (
            df.groupby(
                ["site_id", "site_name", "latitude", "longitude", "country"],
                as_index=False,
            )
            .agg(
                mean_cri=("conservation_risk_index", "mean"),
                volume_count=("volume_id", "count"),
            )
        )
        fig_map = px.scatter_mapbox(
            site_agg,
            lat="latitude",
            lon="longitude",
            size="volume_count",
            color="mean_cri",
            hover_name="site_name",
            hover_data={"mean_cri": ":.1f", "volume_count": True},
            color_continuous_scale="YlOrRd",
            zoom=3,
            height=480,
            title="Mean conservation risk by site",
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map, use_container_width=True)

        if not timeseries.empty:
            ts = timeseries.merge(
                df[["site_id", "site_name"]].drop_duplicates(),
                on="site_id",
            )
            site_pick = st.selectbox(
                "Site for environmental time series",
                sorted(ts["site_name"].unique()),
            )
            ts_site = ts[ts["site_name"] == site_pick]
            fig_env = go.Figure()
            fig_env.add_trace(
                go.Scatter(
                    x=ts_site["month"],
                    y=ts_site["avg_relative_humidity_pct"],
                    name="RH %",
                    yaxis="y",
                )
            )
            fig_env.add_trace(
                go.Scatter(
                    x=ts_site["month"],
                    y=ts_site["avg_temperature_c"],
                    name="Temperature °C",
                    yaxis="y2",
                )
            )
            fig_env.update_layout(
                title=f"Environmental evolution — {site_pick}",
                yaxis=dict(title="RH %"),
                yaxis2=dict(title="°C", overlaying="y", side="right"),
                legend=dict(orientation="h"),
                height=400,
            )
            st.plotly_chart(fig_env, use_container_width=True)

            risk_ts = (
                df.groupby(["site_id", "century"])["conservation_risk_index"]
                .mean()
                .reset_index()
            )
            fig_time = px.line(
                risk_ts,
                x="century",
                y="conservation_risk_index",
                color="site_id",
                title="Mean CRI by century (aggregated profiles)",
                markers=True,
            )
            st.plotly_chart(fig_time, use_container_width=True)

    with tab3:
        st.subheader("From aggregate to individual volume")
        site_options = df[["site_id", "site_name"]].drop_duplicates().sort_values("site_name")
        site_label = st.selectbox(
            "Select site",
            site_options["site_name"].tolist(),
        )
        site_id = site_options.loc[site_options["site_name"] == site_label, "site_id"].iloc[0]
        site_df = df[df["site_id"] == site_id].sort_values(
            "conservation_risk_index", ascending=False
        )
        st.dataframe(
            site_df[
                [
                    "volume_id",
                    "title",
                    "century",
                    "support_material",
                    "conservation_risk_index",
                    "risk_level",
                    "observed_condition_score",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        vol = st.selectbox("Volume detail", site_df["volume_id"].tolist())
        row = site_df[site_df["volume_id"] == vol].iloc[0]
        d1, d2, d3 = st.columns(3)
        d1.metric("CRI", f"{row['conservation_risk_index']:.1f}")
        d2.metric("Risk level", row["risk_level"])
        d3.metric("Observed condition (1–5)", int(row["observed_condition_score"]))
        st.json(
            {
                "Materials": {
                    "support": row["support_material"],
                    "ink": row["ink_type"],
                    "binding": row["binding_type"],
                    "cover": row["cover_type"],
                },
                "Environment": {
                    "temperature_c": row["avg_temperature_c"],
                    "rh_pct": row["avg_relative_humidity_pct"],
                    "light_lux": row["avg_light_lux"],
                    "aqi": int(row["air_quality_index"]),
                },
                "Events": {
                    "flood": bool(row["flood_event"]),
                    "hvac_failure": bool(row["hvac_failure_event"]),
                    "recent_restoration": bool(row["restoration_recent"]),
                },
            }
        )

    with tab4:
        st.subheader("What-if simulation")
        st.write(
            "Adjust environmental parameters for a **reference volume** "
            "to estimate the impact on CRI (same material and age)."
        )
        ref = df.iloc[0].copy()
        baseline_cri = float(ref["conservation_risk_index"])
        c1, c2, c3 = st.columns(3)
        sim_temp = c1.slider("Temperature (°C)", 14.0, 28.0, float(ref["avg_temperature_c"]))
        sim_rh = c2.slider("Relative humidity (%)", 30.0, 75.0, float(ref["avg_relative_humidity_pct"]))
        sim_light = c3.slider("Light (lux)", 5.0, 120.0, float(ref["avg_light_lux"]))
        ref["avg_temperature_c"] = sim_temp
        ref["avg_relative_humidity_pct"] = sim_rh
        ref["avg_light_lux"] = sim_light
        new_cri = compute_cri(ref)
        delta = new_cri - baseline_cri
        st.metric(
            "Simulated CRI",
            f"{new_cri:.1f}",
            delta=f"{delta:+.1f} vs baseline",
        )

        st.subheader("Priority intervention ranking")
        top_n = st.slider("Top N volumes", 5, 50, 15)
        priority = df.nlargest(top_n, "conservation_risk_index")[
            [
                "volume_id",
                "site_name",
                "century",
                "support_material",
                "conservation_risk_index",
                "risk_level",
                "avg_relative_humidity_pct",
            ]
        ]
        st.dataframe(priority, use_container_width=True, hide_index=True)


def main() -> None:
    books, timeseries = load_data()
    sidebar_filters(books)
    filtered = apply_filters(books)
    if filtered.empty:
        st.warning("No records match the current filters.")
        return
    main_dashboard(filtered, timeseries)


if __name__ == "__main__":
    main()
