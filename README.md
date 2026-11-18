# 🎵 MoodMatch AI — Music Recommendation System

## Project Summary

MoodMatch AI is a content-based music recommendation system that helps listeners discover songs based on their preferred genre, mood, and energy level.

The application uses a catalog of 18 songs, scores recommendations, checks their quality, and explores alternative preferences when a playlist contains fewer than five qualifying songs.

This project extends my original CodePath Module 3 music recommender by adding an agentic decision workflow and a reliability system.

## Original Project — CodePath Module 3

My original project was the Music Recommender Simulation from CodePath AI110 Module 3.

It used content-based filtering to compare song features against a listener's favorite genre, favorite mood, and target energy. The system ranked songs using a weighted scoring formula and returned the five highest-scoring songs with explanations.

The original application demonstrated recommendations for four example listener profiles using a catalog of 18 songs.

## New Features Added in Project 4

### Option 2 — Agentic Workflow

I added a multi-step, rule-based agent in `src/agent.py`.

The agent:

1. Generates an initial playlist.
2. Checks how many recommendations meet the quality threshold.
3. Detects when the playlist has fewer than five qualifying songs.
4. Explores alternative genre and mood combinations.
5. Compares alternatives based on the number of qualifying songs.
6. Reports an alternative when it finds more qualifying songs.
7. Preserves the user's original preferences.
8. Records its decisions for inspection.

For example, a happy pop request may produce two qualifying songs. The agent can identify an alternative combination such as adventurous lofi that produces three qualifying songs.

The alternative is a suggestion, not an automatic replacement. More qualifying songs under different preferences does not necessarily mean a better match for the original listener.

This is a rule-based decision workflow, not a large language model.

### Option 4 — Reliability and Evaluation System

I added reliability checks in `src/reliability.py`.

The system:

- Validates user preferences before generating recommendations.
- Rejects invalid inputs, including energy values outside the allowed range.
- Filters recommendations with scores below 2.0.
- Evaluates how many songs pass the quality threshold.
- Generates a quality report.
- Uses automated tests to verify expected behavior.

The quality pass rate measures the percentage of evaluated songs meeting the score threshold. It does not measure recommendation accuracy or actual listener satisfaction.

## How the Recommendation System Works

MoodMatch AI uses content-based filtering rather than collaborative filtering because the dataset includes song features but does not include listening histories from multiple users.

Each song includes a genre, mood, and energy level.

The scoring formula is:

- Matching genre: +2.0 points
- Matching mood: +1.0 point
- Energy similarity: `1 - abs(song_energy - target_energy)`

Songs are ranked from highest to lowest score.

The reliability system removes recommendations scoring below 2.0. Consequently, a playlist may contain fewer than five songs.

The agent explores alternative preferences when the original playlist is short.

## Architecture Overview

The system contains four main components:

- `src/main.py` — Runs the four example profiles, displays recommendations and quality reports, and saves decision logs.
- `src/recommender.py` — Loads songs, calculates scores, ranks songs, and filters weak matches.
- `src/agent.py` — Coordinates the recommendation workflow and explores alternatives.
- `src/reliability.py` — Validates inputs and evaluates recommendation quality.

The application reads the song catalog from `data/songs.csv`.

Automated tests are located in the `tests/` directory.

The system architecture diagram is available in [architecture.mmd](src/diagrams/architecture.mmd)

The agent's decision logs are saved in [ai_interactions.md](ai_interactions.md).

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/rxjj/moodmatch-ai.git
cd moodmatch-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run MoodMatch AI

```bash
python -m src.main
```

The application processes four example profiles and displays recommendations, quality reports, and agent decisions.

It also writes the agent's decision logs to `ai_interactions.md`.

### 5. Run Automated Tests

```bash
python -m pytest -q
```

Latest local test result:

```text
15 passed in 0.10s
```

## Sample Interactions

The following examples use the four profiles configured in `src/main.py`.

### Example 1 — High-Energy Pop

Input:

```python
{
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85
}
```

Recommendation output:

```text
MoodMatch AI — High-Energy Pop
Qualifying recommendations: 2

Sunrise City - Score: 3.97
Gym Hero - Score: 2.92

Playlist Quality Report
Songs evaluated: 18
Songs meeting threshold: 2
Quality pass rate: 11%
Minimum score required: 2.0
```

Agent behavior:

The agent detects a short playlist, explores alternative genres and moods, and reports an alternative with more qualifying songs while preserving the original preferences.

### Example 2 — Chill Lofi

Input:

```python
{
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4
}
```

Recommendation output:

```text
MoodMatch AI — Chill Lofi
Qualifying recommendations: 3

Midnight Coding - Score: 3.98
Library Rain - Score: 3.95
Focus Flow - Score: 3.00

Playlist Quality Report
Songs evaluated: 18
Songs meeting threshold: 3
Quality pass rate: 17%
Minimum score required: 2.0
```

### Example 3 — Deep Intense Rock

Input:

```python
{
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.95
}
```

Recommendation output:

```text
MoodMatch AI — Deep Intense Rock
Qualifying recommendations: 1

Storm Runner - Score: 3.96

Playlist Quality Report
Songs evaluated: 18
Songs meeting threshold: 1
Quality pass rate: 6%
Minimum score required: 2.0
```

### Example 4 — High-Energy Melancholic Blues

Input:

```python
{
    "favorite_genre": "blues",
    "favorite_mood": "melancholic",
    "target_energy": 0.95
}
```

Recommendation output:

```text
MoodMatch AI — High-Energy Melancholic Blues (Edge Case)
Qualifying recommendations: 1

Blue Hour Train - Score: 3.51

Playlist Quality Report
Songs evaluated: 18
Songs meeting threshold: 1
Quality pass rate: 6%
Minimum score required: 2.0
```

## Reliability and Guardrail Examples

### Example 1 — Invalid Energy

Input:

```python
{
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 2.0
}
```

Behavior:

The input validator rejects the request because the energy value is outside the allowed range of 0.0 to 1.0.

Result: A `ValueError` is raised rather than processing an invalid preference.

### Example 2 — Filtering Weak Recommendations

Input: A happy pop listener requests five songs.

Behavior: The recommender scores the catalog and removes songs scoring below 2.0.

Result: Only two qualifying recommendations are returned instead of filling the playlist with weaker matches.

### Example 3 — Agent Alternative Exploration

Input: A happy pop listener requests five songs.

Behavior: The agent identifies that only two songs qualify and explores other genre and mood combinations.

Result: It identifies an alternative that produces three qualifying songs, while leaving the original playlist unchanged.

## Design Decisions and Trade-Offs

### Content-Based Recommendations

I chose content-based filtering because the dataset contains song attributes but no listener histories.

The trade-off is that recommendations rely on predefined features rather than learning individual preferences from real feedback.

### Quality Threshold

I used a minimum score of 2.0 to prevent weak recommendations from appearing in the playlist.

The trade-off is that some users receive fewer than five songs.

### Agentic Workflow

I added an agent to explore alternatives when the original playlist is short.

The agent uses deterministic rules, making its decisions easier to inspect and test.

However, it currently prioritizes the number of qualifying songs over similarity to the original preferences.

### Preserving User Preferences

I decided that the agent should suggest alternatives rather than silently replace the original playlist.

This keeps the system transparent and gives the listener control over their preferences.

## Testing Summary

The project uses pytest to test the recommender, reliability system, and agent workflow.

The automated tests cover:

- Generating recommendations
- Validating user preferences
- Rejecting invalid energy values
- Filtering weak matches
- Evaluating recommendation quality
- Detecting short playlists
- Exploring alternatives
- Preserving original preferences
- Verifying agent outputs

All 15 automated tests passed in the latest local run.

During development, an early agent version explored alternative moods but could not improve the number of qualifying songs for the pop profile.

I revised the workflow to explore both genres and moods. The revised version found an alternative with three qualifying songs instead of two.

This demonstrated why testing actual system behavior matters, not just checking whether code runs without errors.

## Reliability and Evaluation Results

| Test Input / Scenario | Expected Behavior | Actual Result |
|---|---|---|
| High-Energy Pop | Filter songs below 2.0 | Pass: 2 qualifying songs |
| Chill Lofi | Filter songs below 2.0 | Pass: 3 qualifying songs |
| Deep Intense Rock | Filter songs below 2.0 | Pass: 1 qualifying song |
| High-Energy Melancholic Blues | Handle limited matches | Pass: 1 qualifying song |
| Invalid preferences | Reject invalid inputs | Pass: Validation tests passed |
| Short playlist | Agent explores alternatives | Pass: Found an alternative with 3 songs |
| Final quality check | Verify recommendations meet the threshold | Pass: Final songs met the 2.0 threshold |

## Limitations and Future Improvements

The catalog contains only 18 songs, limiting recommendation variety.

The system uses fixed scoring rules rather than a trained machine-learning model.

It does not use real listening history, user ratings, or listener feedback.

The agent's alternative preferences may differ substantially from the original request.

Future improvements could include:

- Expanding the song catalog 
- Incorporating listening history and user feedback
- Using additional audio features
- Ranking alternatives by similarity to original preferences
- Adding an interactive user interface
- Evaluating recommendations with real listener feedback

## Reflection

This project helped me understand how recommendation systems can combine decision-making workflows with reliability checks.

I learned that a system should not only generate results but also validate inputs, evaluate outputs, and explain its decisions.

My detailed reflection on AI collaboration, accepted and revised suggestions, and responsible AI is documented in [model_card.md](model_card.md).