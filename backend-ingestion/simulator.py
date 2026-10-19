import time
import math
import httpx

INGEST_URL = "http://localhost:8000/api/v1/tracks"

# Seed coordinates (North Sea / The Hague corridor)
tracks = [
    {"id": "NATO-TRK-101", "classification": "FRIENDLY", "lat": 52.0705, "lon": 4.3007, "speed": 420.0, "alt": 8500.0, "angle": 0.0},
    {"id": "AIR-UNKNOWN-202", "classification": "UNKNOWN", "lat": 53.2000, "lon": 5.1000, "speed": 280.0, "alt": 4200.0, "angle": 1.2},
    {"id": "RED-FLAG-999", "classification": "HOSTILE", "lat": 54.5000, "lon": 6.8000, "speed": 580.0, "alt": 11000.0, "angle": 2.5},
]

def step_simulation():
    step = 0
    with httpx.Client(timeout=5.0) as client:
        print("Starting synthetic telemetry streaming to", INGEST_URL)
        while True:
            step += 1
            for t in tracks:
                # Update lat/lon along a circular/linear path
                t["lat"] += 0.005 * math.cos(t["angle"] + (step * 0.05))
                t["lon"] += 0.008 * math.sin(t["angle"] + (step * 0.05))
                heading = (math.degrees(t["angle"] + (step * 0.05)) * 10) % 360

                payload = {
                    "track_id": t["id"],
                    "classification": t["classification"],
                    "latitude": round(t["lat"], 5),
                    "longitude": round(t["lon"], 5),
                    "altitude_m": t["alt"],
                    "speed_knots": t["speed"],
                    "heading_deg": round(heading, 2)
                }

                try:
                    res = client.post(INGEST_URL, json=payload)
                    print(f"[{res.status_code}] Posted {t['id']}: lat={payload['latitude']}, lon={payload['longitude']}")
                except Exception as exc:
                    print(f"Failed to post {t['id']}: {exc}")

            time.sleep(2)

if __name__ == "__main__":
    step_simulation()