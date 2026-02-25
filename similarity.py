import math
import numpy as np
from vibe_profile import SongVibeProfile

WEIGHTS = {
    "c1": 0.25,
    "c2": 0.20,
    "c3": 0.10,
    "c4": 0.10,
    "c5": 0.15,
    "c6": 0.10,
    "c7": 0.10,
}

def d_c1(a: SongVibeProfile, b: SongVibeProfile) -> float:
    dv = a.c1.valence - b.c1.valence
    da = a.c1.arousal - b.c1.arousal
    return math.sqrt(dv*dv + da*da) / math.sqrt(2)

def d_c2(a: SongVibeProfile, b: SongVibeProfile) -> float:
    def to_vec(c2):
        vec = np.zeros(13)
        for eid, strength in c2.top3_moods:
            vec[eid-1] = strength
        return vec
    va = to_vec(a.c2)
    vb = to_vec(b.c2)
    num = float(np.dot(va, vb))
    denom = float(np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9)
    cos_sim = num / denom
    return 1.0 - cos_sim

def d_c3(a: SongVibeProfile, b: SongVibeProfile) -> float:
    dbpm = abs(a.c3.bpm - b.c3.bpm) / 50.0
    ddance = abs(a.c3.danceability - b.c3.danceability)
    dgroove = abs(a.c3.groove_type - b.c3.groove_type) / 5.0
    return min(1.0, dbpm + ddance + dgroove)

def d_c4(a: SongVibeProfile, b: SongVibeProfile) -> float:
    va = np.array([a.c4.brightness, a.c4.warmth, a.c4.density, a.c4.width])
    vb = np.array([b.c4.brightness, b.c4.warmth, b.c4.density, b.c4.width])
    dist = np.linalg.norm(va - vb) / math.sqrt(4)
    return float(min(1.0, dist))

def d_c5(a: SongVibeProfile, b: SongVibeProfile) -> float:
    dsent = abs(a.c5.sentiment - b.c5.sentiment) / 2.0
    dtheme = abs(a.c5.theme_cluster - b.c5.theme_cluster) / 12.0
    dcomp = abs(a.c5.complexity - b.c5.complexity)
    return min(1.0, dsent + dtheme + dcomp)

def d_c6(a: SongVibeProfile, b: SongVibeProfile) -> float:
    va = np.array([a.c6.v1, a.c6.c1, a.c6.v2, a.c6.c2, a.c6.b])
    vb = np.array([b.c6.v1, b.c6.c1, b.c6.v2, b.c6.c2, b.c6.b])
    return float(np.mean(np.abs(va - vb)))

def d_c7(a: SongVibeProfile, b: SongVibeProfile) -> float:
    va = np.array([a.c7.era_code, a.c7.genre_code, a.c7.region_code, a.c7.intent_code])
    vb = np.array([b.c7.era_code, b.c7.genre_code, b.c7.region_code, b.c7.intent_code])
    denom = np.array([10.0, 50.0, 20.0, 8.0])
    return float(np.mean(np.abs(va - vb) / denom))

def similarity(a: SongVibeProfile, b: SongVibeProfile) -> float:
    return (
        WEIGHTS["c1"] * d_c1(a, b) +
        WEIGHTS["c2"] * d_c2(a, b) +
        WEIGHTS["c3"] * d_c3(a, b) +
        WEIGHTS["c4"] * d_c4(a, b) +
        WEIGHTS["c5"] * d_c5(a, b) +
        WEIGHTS["c6"] * d_c6(a, b) +
        WEIGHTS["c7"] * d_c7(a, b)
    )

def find_similar(seed: SongVibeProfile,
                 candidates: list[SongVibeProfile],
                 max_results: int = 10,
                 threshold: float = 0.3):
    scored = [(c, similarity(seed, c)) for c in candidates]
    scored = [x for x in scored if x[1] < threshold]
    scored.sort(key=lambda x: x[1])
    return scored[:max_results]