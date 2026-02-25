from vibe_profile import C1EmotionalCore, C3TempoGroove

def extract_c1_c3_from_spotify(sp, track_id: str) -> tuple[C1EmotionalCore, C3TempoGroove]:
    features_list = sp.audio_features([track_id])
    features = features_list[0]

    c1 = C1EmotionalCore(
        valence=float(features["valence"]),
        arousal=float(features["energy"]),  # energy as arousal proxy
    )

    c3 = C3TempoGroove(
        bpm=float(features["tempo"]),
        danceability=float(features["danceability"]),
        groove_type=1,  # default Straight; refine later
    )

    return c1, c3