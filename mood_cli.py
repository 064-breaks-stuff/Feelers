from vibe_profile import C2MoodFingerprint

EMOTIONS = {
    1: "Amusing",
    2: "Annoying",
    3: "Anxious",
    4: "Beautiful",
    5: "Calm",
    6: "Dreamy",
    7: "Energizing",
    8: "Erotic",
    9: "Indignant",
    10: "Joyful",
    11: "Sad",
    12: "Scary",
    13: "Triumphant",
}

def annotate_c2_cli() -> C2MoodFingerprint:
    print("\nPick top 3 emotions (ID + strength 0.0–1.0):")
    for k, v in EMOTIONS.items():
        print(f"{k}: {v}")
    moods = []
    for i in range(3):
        eid = int(input(f"Emotion #{i+1} ID: "))
        strength = float(input(f"Emotion #{i+1} strength: "))
        moods.append((eid, strength))
    return C2MoodFingerprint(top3_moods=moods)
