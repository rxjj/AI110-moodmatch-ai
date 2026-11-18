import pytest

from src.recommender import recommend_songs
from src.reliability import (
    validate_preferences,
    evaluate_recommendations,
    filter_recommendations,
)


@pytest.fixture
def preferences():
    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }


def test_valid_preferences(preferences):
    validate_preferences(preferences, k=5)


def test_invalid_energy(preferences):
    preferences["target_energy"] = 1.5

    with pytest.raises(ValueError):
        validate_preferences(preferences)


def test_missing_genre(preferences):
    del preferences["favorite_genre"]

    with pytest.raises(ValueError):
        validate_preferences(preferences)


def test_invalid_recommendation_count(preferences):
    with pytest.raises(ValueError):
        validate_preferences(preferences, k=0)


def test_filter_removes_weak_matches():
    recommendations = [
        ({"title": "Strong Song"}, 3.5, "Good match"),
        ({"title": "Weak Song"}, 0.8, "Poor match"),
    ]

    filtered = filter_recommendations(recommendations)

    assert len(filtered) == 1
    assert filtered[0][0]["title"] == "Strong Song"


def test_evaluation_pass_rate(preferences):
    recommendations = [
        ({"title": "Song A"}, 3.5, "Good match"),
        ({"title": "Song B"}, 2.5, "Good match"),
        ({"title": "Song C"}, 0.5, "Weak match"),
    ]

    report = evaluate_recommendations(preferences, recommendations)

    assert report["total"] == 3
    assert report["passing"] == 2
    assert report["pass_rate"] == 0.67


def test_recommender_filters_weak_songs(preferences):
    songs = [
        {"title": "Happy Pop", "genre": "pop", "mood": "happy", "energy": 0.9},
        {"title": "Unrelated Song", "genre": "rock", "mood": "sad", "energy": 0.9},
    ]

    results = recommend_songs(preferences, songs, k=5)

    assert len(results) == 1
    assert results[0][0]["title"] == "Happy Pop"


def test_empty_song_list(preferences):
    results = recommend_songs(preferences, [], k=5)

    assert results == []
