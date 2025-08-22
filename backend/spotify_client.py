import os
import time
import requests
import random
from urllib.parse import quote_plus
from dotenv import load_dotenv


load_dotenv()


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
MIN_POPULARITY = int(os.getenv("SPOTIFY_MIN_POPULARITY" , "50"))


_TOKEN = None
_TOKEN_EXPIRES = 0


TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"




def _get_client_token():

    global _TOKEN, _TOKEN_EXPIRES
    if _TOKEN and time.time() < _TOKEN_EXPIRES - 60:
        return _TOKEN


    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise RuntimeError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")


    resp = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    resp.raise_for_status()
    data = resp.json()
    _TOKEN = data["access_token"]
    _TOKEN_EXPIRES = time.time() + data.get("expires_in", 3600)
    return _TOKEN




def _build_query(genre=None, time_period=None):
    parts = []
    if genre:
        # Spotify search supports genre: but it's more reliable for artists; we include it anyway
        parts.append(f"genre:{quote_plus(genre)}")


    if time_period:
        # Accept many formats: "1990s", "2000-2010", "1995", "1990-1999"
        # We'll try to translate simple forms
        if "s" in time_period and time_period.endswith("s"):
            decade = time_period[:-1]
            # e.g. 1990s -> 1990-1999
            if decade.isdigit():
                parts.append(f"year:{decade}-{int(decade)+9}")
        elif "-" in time_period:
            # assume valid
            parts.append(f"year:{time_period}")
        elif time_period.isdigit():
            parts.append(f"year:{time_period}")


    if not parts:
    # No filter: pick a broad range so Spotify returns lots of items
    # Use a wide year range
        parts.append("year:1900-2025")


    # combine using spaces (Spotify treats space as AND)
    return " ".join(parts)




def search_tracks(genre=None, time_period=None, limit=50):
    """Search Spotify tracks and return up to `limit` candidate tracks (dicts).
    We'll fetch multiple pages if available but keep it simple.
    """
    token = _get_client_token()
    headers = {"Authorization": f"Bearer {token}"}


    q = _build_query(genre, time_period)
    params = {"q": q, "type": "track", "limit": min(limit, 50)}


    r = requests.get(SEARCH_URL, headers=headers, params=params)
    r.raise_for_status()
    data = r.json()
    tracks = data.get("tracks", {}).get("items", [])
    return tracks




def get_random_songs(genre=None, time_period=None, count=10, min_popularity=MIN_POPULARITY):
    # Fetch a batch (50) and filter by popularity, then sample
    candidates = search_tracks(genre, time_period, limit=50)
    # filter
    filtered = [t for t in candidates if (t.get("popularity") or 0) >= min_popularity]


    if len(filtered) < count:
        # fallback: relax threshold and/or fetch again without filters
        candidates2 = search_tracks(genre, time_period, limit=50)
        merged = {t['id']: t for t in (filtered + candidates2)}
        filtered = list(merged.values())


    if not filtered:
        return []


    random.shuffle(filtered)
    chosen = filtered[:count]


    # map to simple dicts
    out = []
    for t in chosen:
        out.append({
            "id": t.get("id"),
            "name": t.get("name"),
            "artists": [a.get("name") for a in t.get("artists", [])],
            "album": t.get("album", {}).get("name"),
            "popularity": t.get("popularity"),
            "spotify_url": t.get("external_urls", {}).get("spotify"),
        })
    return out