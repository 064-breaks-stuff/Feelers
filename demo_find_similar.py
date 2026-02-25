import json
from auth import get_spotify_client
from build_profile import build_profile_for_track
from vibe_profile import profile_from_dict, profile_to_dict
from similarity import find_similar

LIBRARY_FILE = "library_profiles.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [profile_from_dict(d) for d in raw]
    except FileNotFoundError:
        return []

def save_library(profiles):
    raw = [profile_to_dict(p) for p in profiles]
    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

def main():
    sp = get_spotify_client()

    # 1) Build seed profile
    seed_input = input("Enter seed track ID or URL: ").strip()
    if "spotify.com" in seed_input:
        seed_id = seed_input.split("/")[-1].split("?")[0]
    else:
        seed_id = seed_input

    seed_profile = build_profile_for_track(seed_id)

    # 2) Load candidate library
    candidates = load_library()

    # 3) Optionally add this seed to library
    add_lib = input("Add this song to library? (y/n): ").lower()
    if add_lib == "y":
        candidates.append(seed_profile)
        save_library(candidates)

    # 4) Find similar
    matches = find_similar(seed_profile, candidates)

    print("\nTop similar songs:")
    for p, score in matches:
        print(f"{p.name} — {p.artist} (score={score:.3f})")

    # 5) Build a Spotify playlist from matches
    if matches:
        ans = input("\nCreate playlist with these matches? (y/n): ").lower()
        if ans == "y":
            user_id = sp.me()["id"]
            name = input("Playlist name (Enter for default): ").strip()
            if not name:
                name = f"Vibe matches: {seed_profile.name}"
            playlist = sp.user_playlist_create(user=user_id, name=name, public=True)
            uris = [m[0].spotify_id if m[0].spotify_id.startswith("spotify:track")
                    else f"spotify:track:{m[0].spotify_id}" for m in matches]
            sp.playlist_add_items(playlist["id"], uris)
            print(f"Playlist created: {playlist['external_urls']['spotify']}")

if __name__ == "__main__":
    main()
