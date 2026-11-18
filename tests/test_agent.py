import pytest

from src.agent import build_playlist
from src.recommender import load_songs
from src.reliability import evaluate_recommendations


@pytest.fixture
def songs():
    return load_songs("data/songs.csv")


@pytest.fixture
def preferences():
    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
    }


def test_agent_generates_playlist(songs, preferences):
    playlist, decisions = build_playlist(preferences, songs)

    assert len(playlist) == 2
    assert len(decisions) > 0


def test_agent_preserves_original_preferences(songs, preferences):
    original = preferences.copy()

    build_playlist(preferences, songs)

    assert preferences == original


def test_agent_explores_alternatives(songs, preferences):
    _, decisions = build_playlist(preferences, songs)

    assert any(
        "Exploring alternative genres and moods" in decision
        for decision in decisions
    )
    assert any(
        "Better alternative found" in decision
        for decision in decisions
    )


def test_agent_keeps_reliability_checks(songs, preferences):
    playlist, decisions = build_playlist(preferences, songs)

    report = evaluate_recommendations(preferences, playlist)

    assert report["passing"] == report["total"]
    assert all(score >= 2.0 for _, score, _ in playlist)
    assert any("Final verification" in d for d in decisions)


def test_agent_rejects_invalid_input(songs):
    invalid_preferences = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 2.0,
    }

    with pytest.raises(ValueError):
        build_playlist(invalid_preferences, songs)
