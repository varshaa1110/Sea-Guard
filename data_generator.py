"""
data_generator.py — Synthetic AIS Dataset Generator for SEA GUARD

Generates realistic maritime ship data with:
  • 50 unique ships spread across India's EEZ
  • Timestamps spanning now → 1 month ago
  • Random AIS ON/OFF status (~20 % OFF for dark-ship simulation)
  • Some ships with suspicious speeds (< 1 or > 30 knots)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ── reproducibility ──────────────────────────────────────────────────────────
np.random.seed(42)

# ── constants ────────────────────────────────────────────────────────────────
NUM_SHIPS = 50
RECORDS_PER_SHIP = 8          # multiple timestamps per vessel

# India EEZ approximate bounding box
LAT_MIN, LAT_MAX = 6.0, 22.0
LON_MIN, LON_MAX = 68.0, 90.0

# time offsets for realistic spread
TIME_OFFSETS = [
    timedelta(minutes=0),
    timedelta(minutes=15),
    timedelta(minutes=30),
    timedelta(hours=1),
    timedelta(hours=6),
    timedelta(days=1),
    timedelta(weeks=1),
    timedelta(days=30),
]


def generate_dataset() -> pd.DataFrame:
    """Return a DataFrame of synthetic AIS ship records."""
    rows = []
    now = datetime.now()

    for i in range(1, NUM_SHIPS + 1):
        ship_id = f"SHIP-{i:03d}"

        # base position — small jitter added per record for movement
        base_lat = np.random.uniform(LAT_MIN, LAT_MAX)
        base_lon = np.random.uniform(LON_MIN, LON_MAX)

        for j in range(RECORDS_PER_SHIP):
            offset = TIME_OFFSETS[j % len(TIME_OFFSETS)]
            timestamp = now - offset

            # speed: mostly 3–25 knots; ~15 % suspicious
            roll = np.random.random()
            if roll < 0.07:
                speed = round(np.random.uniform(0.0, 0.9), 1)   # very slow
            elif roll < 0.15:
                speed = round(np.random.uniform(31.0, 45.0), 1)  # very fast
            else:
                speed = round(np.random.uniform(3.0, 25.0), 1)

            # AIS status — ~20 % chance OFF
            ais_status = "OFF" if np.random.random() < 0.20 else "ON"

            # small position jitter to simulate movement
            lat = round(base_lat + np.random.uniform(-0.05, 0.05), 4)
            lon = round(base_lon + np.random.uniform(-0.05, 0.05), 4)

            rows.append({
                "ship_id": ship_id,
                "latitude": lat,
                "longitude": lon,
                "speed": speed,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ais_status": ais_status,
            })

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def save_dataset(path: str = "ship_data.csv") -> str:
    """Generate and persist the dataset to *path*; return the path."""
    df = generate_dataset()
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    out = save_dataset()
    print(f"✅  Dataset saved to {out}")
