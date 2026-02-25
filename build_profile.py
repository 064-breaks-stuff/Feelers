from auth import get_spotify_client
from vibe_profile import SongVibeProfile, C4TimbreProfile, C6EnergyArc
from features_spotify import extract_c1_c3_from_spotify
from features_audio import extract_c4_c6_from_preview
from mood_cli import annotate_c2_cli
from lyrics_sentiment import extract_c5_from_lyrics
from context_cli import annotate_c7_cli

def build_profile_for_track(track_id: str) -> SongVibeProfile:
    sp = get_spotify_client()
    track = sp.track(track_id)
    name = track["name"]
    artist = track["artists"][0]["name"]

    c1, c3 = extract_c1_c3_from_spotify(sp, track_id)

    preview_url = track.get("preview_url")
    if preview_url:
        c4, c6 = extract_c4_c6_from_preview(preview_url)
    else:
        c4 = C4TimbreProfile(0.5, 0.5, 0.5, 0.5)
        c6 = C6EnergyArc(0.3, 0.5, 0.4, 0.6, 0.7)

    print(f"\nAnnotating moods for: {name} — {artist}")
    c2 = annotate_c2_cli()

    print("\nPaste lyrics (end with empty line):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    lyrics = "\n".join(lines)
    c5 = extract_c5_from_lyrics(lyrics)

    print("\nAnnotate context codes:")
    c7 = annotate_c7_cli()

    return SongVibeProfile(
        spotify_id=track_id,
        name=name,
        artist=artist,
        c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7,
    )

if __name__ == "__main__":
    tid = input("Enter Spotify track ID or URL: ").strip()
    if "spotify.com" in tid:
        tid = tid.split("/")[-1].split("?")[0]
    profile = build_profile_for_track(tid)
    print("\nBuilt profile:")
    print(profile)
