"""
MoodMatch AI — Music Recommendation System

Runs the recommendation system with:
Option 2: Agentic decision-making workflow
Option 4: Reliability checks and evaluation
"""

from pathlib import Path

from .agent import build_playlist
from .recommender import load_songs, score_song
from .reliability import evaluate_recommendations


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        (
            "High-Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.85,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.4,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.95,
            },
        ),
        (
            "High-Energy Melancholic Blues (Edge Case)",
            {
                "favorite_genre": "blues",
                "favorite_mood": "melancholic",
                "target_energy": 0.95,
            },
        ),
    ]

    # Collect agent decisions for the project log.
    interaction_logs = [
        "# MoodMatch AI — Agent Decision Logs",
        "",
        "These logs record the agent's decision steps.",
        "The workflow uses rule-based decisions, not an LLM.",
        "",
    ]

    total_profiles = 0
    profiles_passing = 0

    for profile_name, user_prefs in profiles:

        # Option 2 generates and evaluates recommendations.
        recommendations, decisions = build_playlist(
            user_prefs, songs, k=5
        )

        print(f"\nMoodMatch AI — {profile_name}")
        print(f"Qualifying recommendations: {len(recommendations)}\n")

        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()

        # Option 4 evaluates all songs against original preferences.
        all_scored = []
        for song in songs:
            score, reasons = score_song(user_prefs, song)
            all_scored.append((song, score, " ".join(reasons)))

        report = evaluate_recommendations(user_prefs, all_scored)

        total_profiles += 1

        if recommendations and all(score >= report["threshold"] for _, score, _ in recommendations):
            profiles_passing += 1

        print("Playlist Quality Report")
        print(f"Songs evaluated: {report['total']}")
        print(f"Songs meeting threshold: {report['passing']}")
        print(f"Quality pass rate: {report['pass_rate']:.0%}")
        print(f"Minimum score required: {report['threshold']:.1f}")

        print("\nAgent Decision Log")
        for decision in decisions:
            print(f"- {decision}")

        # Save the decision chain in Markdown.
        interaction_logs.append(f"## {profile_name}")
        interaction_logs.append("")
        for decision in decisions:
            interaction_logs.append(f"- {decision}")
        interaction_logs.append("")

        print("-" * 45)

    
    Path("ai_interactions.md").write_text(
        "\n".join(interaction_logs),
        encoding="utf-8"
    )

    print("\nAgent decision logs saved to ai_interactions.md")

    print("\n=== Final Evaluation Summary ===")
    print(f"Profiles evaluated: {total_profiles}")
    print(f"Profiles passing quality checks: {profiles_passing}")
    print(f"Profiles failing quality checks: {total_profiles - profiles_passing}")

if __name__ == "__main__":
    main()

