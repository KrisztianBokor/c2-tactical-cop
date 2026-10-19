import os
import datetime
from typing import Literal
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import asyncpg
import redis.asyncio as redis

# Environment configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://nato_operator:operator_secret@localhost:5432/c2_tactical"
)

# Global connections
db_pool: asyncpg.Pool | None = None
redis_client: redis.Redis | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool, redis_client
    # Startup: create connection pools
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    yield
    # Shutdown: clean close
    if db_pool:
        await db_pool.close()
    if redis_client:
        await redis_client.close()


app = FastAPI(
    title="C2 Tactical Ingestion Service",
    description="High-throughput telemetry ingestion with Redis caching & PostGIS spatial persistence.",
    version="1.0.0",
    lifespan=lifespan
)


class TelemetryTrack(BaseModel):
    track_id: str = Field(..., example="NATO-TRK-102", min_length=3, max_length=32)
    classification: Literal["FRIENDLY", "HOSTILE", "UNKNOWN"] = Field(..., example="FRIENDLY")
    latitude: float = Field(..., ge=-90.0, le=90.0, example=52.0705)
    longitude: float = Field(..., ge=-180.0, le=180.0, example=4.3007)
    altitude_m: float = Field(default=0.0, ge=0.0, le=100000.0, example=9500.0)
    speed_knots: float = Field(default=0.0, ge=0.0, le=3000.0, example=450.0)
    heading_deg: float = Field(default=0.0, ge=0.0, le=360.0, example=120.5)


@app.get("/health", tags=["Monitoring"])
async def health_check():
    return {"status": "HEALTHY", "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}


@app.post("/api/v1/tracks", status_code=status.HTTP_202_ACCEPTED, tags=["Telemetry"])
async def ingest_track(track: TelemetryTrack):
    if not redis_client or not db_pool:
        raise HTTPException(status_code=503, detail="Datastores not initialized")

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # 1. Update Hot State in Redis
    redis_key = f"track:{track.track_id}"
    await redis_client.hset(
        redis_key,
        mapping={
            "track_id": track.track_id,
            "classification": track.classification,
            "latitude": str(track.latitude),
            "longitude": str(track.longitude),
            "altitude_m": str(track.altitude_m),
            "speed_knots": str(track.speed_knots),
            "heading_deg": str(track.heading_deg),
            "updated_at": now_iso
        }
    )

    # 2. Persist historical track point in PostGIS
    insert_sql = """
        INSERT INTO asset_tracks (
            track_id, classification, speed_knots, altitude_m, heading_deg, location
        )
        VALUES (
            $1, $2, $3, $4, $5, ST_SetSRID(ST_MakePoint($6, $7), 4326)
        );
    """
    async with db_pool.acquire() as conn:
        await conn.execute(
            insert_sql,
            track.track_id,
            track.classification,
            track.speed_knots,
            track.altitude_m,
            track.heading_deg,
            track.longitude,  # ST_MakePoint takes (X, Y) -> (Longitude, Latitude)
            track.latitude
        )

    return {"status": "ACCEPTED", "track_id": track.track_id}


@app.get("/api/v1/tracks/{track_id}", tags=["Telemetry"])
async def get_live_track(track_id: str):
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis connection unavailable")

    data = await redis_client.hgetall(f"track:{track_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Track not found in live cache")
    return data