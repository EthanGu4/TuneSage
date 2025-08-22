from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from spotify_client import get_random_songs
from database import SessionLocal, engine, metadata
import os

app = FastAPI(title="Music of the Day Bot API")

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Music of the Day Bot API! Use /songs endpoint."}

@app.get("/songs")
async def songs(
    genre: Optional[str] = Query(None, description="Optional genre"),
    time_period: Optional[str] = Query(None, description="Optional time period (e.g. 1990s, 2000-2010)"),
    count: int = Query(10, ge=1, le=50),
):
    
    """
    Returns random songs from Spotify.  
    Optional filters: genre, time_period.  
    Default count = 10 songs.
    """
    results = get_random_songs(genre, time_period, count=count)
    return {"count": len(results), "results": results}