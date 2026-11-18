from .recommender import recommend_songs
from .reliability import validate_preferences, evaluate_recommendations


def build_playlist(user_prefs, songs, k=5):
    """Generate, evaluate, and suggest an improved playlist."""
    validate_preferences(user_prefs, k)
    decisions = []

    # 1. Generate the original playlist.
    playlist = recommend_songs(user_prefs, songs, k)
    report = evaluate_recommendations(user_prefs, playlist)

    decisions.append(
        f"Original playlist: {len(playlist)} of {k} songs."
    )
    decisions.append(
        f"Quality check: {report['passing']} of "
        f"{report['total']} songs passed."
    )

    # 2. Explore alternatives if the playlist is short.
    if len(playlist) < k:
        decisions.append(
            "Playlist is short. Exploring alternative genres and moods."
        )

        best_prefs = None
        best_playlist = playlist
        best_count = len(playlist)

        available_genres = sorted({
            song["genre"] for song in songs
        })
        available_moods = sorted({
            song["mood"] for song in songs
        })

        # 3. Try combinations of available genres and moods.
        for genre in available_genres:
            for mood in available_moods:
                if (
                    genre == user_prefs["favorite_genre"]
                    and mood == user_prefs["favorite_mood"]
                ):
                    continue

                alternative_prefs = dict(user_prefs)
                alternative_prefs["favorite_genre"] = genre
                alternative_prefs["favorite_mood"] = mood

                candidate_playlist = recommend_songs(
                    alternative_prefs, songs, k
                )

                candidate_report = evaluate_recommendations(
                    alternative_prefs, candidate_playlist
                )

                # 4. Keep the alternative with more valid songs.
                if candidate_report["passing"] > best_count:
                    best_count = candidate_report["passing"]
                    best_prefs = alternative_prefs
                    best_playlist = candidate_playlist

        # 5. Report the best alternative.
        if best_prefs is not None:
            decisions.append(
                "Better alternative found: "
                f"genre='{best_prefs['favorite_genre']}', "
                f"mood='{best_prefs['favorite_mood']}'."
            )
            decisions.append(
                f"Alternative playlist: {best_count} of {k} songs."
            )
            decisions.append(
                "Original preferences remain unchanged."
            )
        else:
            decisions.append(
                "No alternative improved the playlist."
            )

    else:
        decisions.append(
            "Playlist meets the requested song count."
        )

    # 6. Verify the original playlist.
    final_report = evaluate_recommendations(user_prefs, playlist)
    decisions.append(
        f"Final verification: {final_report['passing']} "
        f"of {final_report['total']} songs passed."
    )

    return playlist, decisions

