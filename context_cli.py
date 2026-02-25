from vibe_profile import C7Context

def annotate_c7_cli() -> C7Context:
    print("\nContext codes:")
    era_code = int(input("EraCode (1–10): "))
    genre_code = int(input("GenreCode (1–50): "))
    region_code = int(input("RegionCode (1–20): "))
    intent_code = int(input("IntentCode (1–8): "))
    return C7Context(
        era_code=era_code,
        genre_code=genre_code,
        region_code=region_code,
        intent_code=intent_code,
    )
