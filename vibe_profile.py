from dataclasses import dataclass
from typing import List, Tuple

MoodTriplet = List[Tuple[int, float]]  # [(EmotionID, Strength)]

@dataclass
class C1EmotionalCore:
    valence: float      # 0.0–1.0
    arousal: float      # 0.0–1.0

@dataclass
class C2MoodFingerprint:
    top3_moods: MoodTriplet

@dataclass
class C3TempoGroove:
    bpm: float          # 40–220
    danceability: float # 0.0–1.0
    groove_type: int    # 1–5

@dataclass
class C4TimbreProfile:
    brightness: float   # 0.0–1.0
    warmth: float       # 0.0–1.0
    density: float      # 0.0–1.0
    width: float        # 0.0–1.0

@dataclass
class C5LyricalSentiment:
    sentiment: float    # -1.0–+1.0
    theme_cluster: int  # 1–12
    complexity: float   # 0.0–1.0

@dataclass
class C6EnergyArc:
    v1: float
    c1: float
    v2: float
    c2: float
    b: float

@dataclass
class C7Context:
    era_code: int
    genre_code: int
    region_code: int
    intent_code: int

@dataclass
class SongVibeProfile:
    spotify_id: str
    name: str
    artist: str
    c1: C1EmotionalCore
    c2: C2MoodFingerprint
    c3: C3TempoGroove
    c4: C4TimbreProfile
    c5: C5LyricalSentiment
    c6: C6EnergyArc
    c7: C7Context

import json
from dataclasses import asdict

def profile_to_dict(p: SongVibeProfile) -> dict:
    return asdict(p)

def profile_from_dict(d: dict) -> SongVibeProfile:
    # Simple reconstruct using unpacking
    return SongVibeProfile(
        spotify_id=d["spotify_id"],
        name=d["name"],
        artist=d["artist"],
        c1=C1EmotionalCore(**d["c1"]),
        c2=C2MoodFingerprint(top3_moods=d["c2"]["top3_moods"]),
        c3=C3TempoGroove(**d["c3"]),
        c4=C4TimbreProfile(**d["c4"]),
        c5=C5LyricalSentiment(**d["c5"]),
        c6=C6EnergyArc(**d["c6"]),
        c7=C7Context(**d["c7"]),
    )
