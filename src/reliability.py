"""Reliability checks for MoodMatch AI music recommendations."""

import math


def validate_preferences(user_prefs, k=5):
    """Check user preferences before generating recommendations."""
    required = ("favorite_genre", "favorite_mood", "target_energy")

    if not isinstance(user_prefs, dict):
        raise ValueError("Preferences must be a dictionary.")

    for field in required:
        if field not in user_prefs:
            raise ValueError(f"Missing required preference: {field}")

    for field in ("favorite_genre", "favorite_mood"):
        value = user_prefs[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string.")

    energy = user_prefs["target_energy"]
    if (
        isinstance(energy, bool)
        or not isinstance(energy, (int, float))
        or not math.isfinite(energy)
        or not 0 <= energy <= 1
    ):
        raise ValueError("target_energy must be between 0 and 1.")

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer.")


def evaluate_recommendations(user_prefs, recommendations, threshold=2.0):
    """Measure how many recommended songs meet the quality threshold."""
    if not 0 <= threshold <= 4:
        raise ValueError("threshold must be between 0 and 4.")

    total = len(recommendations)
    passing = sum(
        1 for song, score, explanation in recommendations
        if score >= threshold
    )

    pass_rate = passing / total if total else 0.0

    return {
        "total": total,
        "passing": passing,
        "pass_rate": round(pass_rate, 2),
        "threshold": threshold,
    }


def filter_recommendations(recommendations, threshold=2.0):
    """Remove weak recommendations that fall below the threshold."""
    return [
        recommendation
        for recommendation in recommendations
        if recommendation[1] >= threshold
    ]