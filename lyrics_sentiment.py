from nltk.sentiment import SentimentIntensityAnalyzer
from vibe_profile import C5LyricalSentiment

sia = SentimentIntensityAnalyzer()

def _estimate_theme_cluster(text: str) -> int:
    t = text.lower()
    if "love" in t or "heart" in t:
        return 1  # Love
    if "miss you" in t or "gone" in t or "lost" in t:
        return 2  # Loss
    if "fight" in t or "rebel" in t or "against" in t:
        return 3  # Rebellion
    if "party" in t or "tonight" in t or "celebrate" in t:
        return 4  # Celebration
    if "think" in t or "wonder" in t or "why" in t:
        return 5  # Reflection
    if "remember" in t or "back then" in t:
        return 6  # Nostalgia
    # …extend for 7–11…
    return 12  # Abstract default

def extract_c5_from_lyrics(lyrics: str) -> C5LyricalSentiment:
    scores = sia.polarity_scores(lyrics)
    sentiment = float(scores["compound"])  # -1 to +1

    theme_cluster = _estimate_theme_cluster(lyrics)

    words = [w for w in lyrics.split() if any(c.isalpha() for c in w)]
    total_words = len(words) or 1
    unique_words = len(set(words)) or 1
    avg_syllables = sum(len(w) / 3.0 for w in words) / total_words
    raw_complexity = (unique_words / total_words) * avg_syllables
    complexity = float(max(0.0, min(raw_complexity, 1.0)))

    return C5LyricalSentiment(
        sentiment=sentiment,
        theme_cluster=theme_cluster,
        complexity=complexity,
    )