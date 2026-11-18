# 🎧 Model Card: MoodMatch AI

## 1. Model Name

**MoodMatch AI — Music Recommendation System**

This project extends my original CodePath Module 3 Music Recommender Simulation.

## 2. Goal / Task

MoodMatch AI recommends songs based on a listener's favorite genre, favorite mood, and desired energy level.

The system also checks recommendation quality and explores alternative preferences when the original playlist contains fewer than five qualifying songs.

The goal is to demonstrate how a recommendation system can combine content-based filtering, a rule-based agentic workflow, and reliability checks.

## 3. Data Used

The recommender uses a catalog of 18 songs.

Each song contains:

- Genre
- Mood
- Energy
- Tempo
- Valence
- Danceability
- Acousticness

The scoring algorithm currently uses genre, mood, and energy.

There is no real listener history, feedback, or user-rating data.

## 4. Algorithm and System Design

### Original Recommendation Algorithm

The original Module 3 system used content-based filtering.

Each song receives:

- +2.0 points for a matching genre.
- +1.0 point for a matching mood.
- Up to +1.0 point for energy similarity.

Energy similarity is calculated using:

`1 - abs(song_energy - target_energy)`

Songs are ranked from highest to lowest score.

### Project 4 — Option 4: Reliability System

I added a reliability system that:

1. Validates user preferences.
2. Rejects invalid input values.
3. Filters recommendations scoring below 2.0.
4. Evaluates recommendation quality.
5. Supports automated testing.

This prevents the recommender from filling a playlist with songs that do not meet the minimum scoring requirement.

### Project 4 — Option 2: Agentic Workflow

I also added a rule-based agent that:

1. Generates an original playlist.
2. Checks the number of qualifying songs.
3. Detects when fewer than five songs qualify.
4. Explores alternative genre and mood combinations.
5. Compares the number of qualifying recommendations.
6. Identifies an alternative when one produces more qualifying songs.
7. Preserves the original user preferences.
8. Records its decisions.

The agent does not use a large language model. It follows a deterministic decision-making workflow.

An alternative with more qualifying songs is not necessarily a better match for the listener's original preferences.

## 5. Observed Behavior and Limitations

The system generally prioritizes songs matching the listener's genre and mood.

However, several limitations remain.

### Small Dataset

The catalog contains only 18 songs.

Some profiles have very few songs that meet the quality threshold.

### Fixed Scoring Rules

Genre, mood, and energy use predefined weights.

The system does not learn from listener behavior.

### Exact Matching

Genre and mood must match exactly.

This may exclude songs that are similar but use different labels.

### Agent Limitations

The agent searches alternative genre and mood combinations to find more qualifying songs.

However, it does not currently measure whether those alternatives are similar to the original preferences.

For example, a happy pop listener may receive a suggestion involving adventurous lofi.

That alternative produces more qualifying songs but may not match the listener's intended musical style.

### Reliability Limitations

A score of 2.0 or higher indicates that a song passes the project's scoring threshold.

It does not prove that a listener will enjoy the song.

The quality pass rate measures threshold compliance, not real-world recommendation accuracy.

## 6. Evaluation Process

I evaluated the system using four example profiles.

### High-Energy Pop

Input:

- Genre: pop
- Mood: happy
- Target energy: 0.85

Results:

- Sunrise City — 3.97
- Gym Hero — 2.92

Two songs met the quality threshold.

The agent identified an alternative preference combination with three qualifying songs.

### Chill Lofi

Input:

- Genre: lofi
- Mood: chill
- Target energy: 0.4

Results:

- Midnight Coding — 3.98
- Library Rain — 3.95
- Focus Flow — 3.00

Three songs met the quality threshold.

### Deep Intense Rock

Input:

- Genre: rock
- Mood: intense
- Target energy: 0.95

Result:

- Storm Runner — 3.96

One song met the quality threshold.

### High-Energy Melancholic Blues

Input:

- Genre: blues
- Mood: melancholic
- Target energy: 0.95

Result:

- Blue Hour Train — 3.51

One song met the quality threshold.

This demonstrates that matching genre and mood can outweigh a weaker energy match.

## 7. Reliability Testing

The project uses pytest to test the recommender, reliability system, and agent workflow.

The latest local test run produced:

```text
15 passed in 0.10s
```

The tests verify:

- Recommendation generation
- Input validation
- Invalid energy rejection
- Quality filtering
- Evaluation reports
- Agent alternative exploration
- Preservation of original preferences
- Final reliability verification

The main application also generates quality reports and saves agent decisions in `ai_interactions.md`.

## 8. Responsible AI Considerations

### Potential Misuse

MoodMatch AI could be misused if someone presents its recommendations as guaranteed to match a listener's tastes.

Because the system uses only 18 songs and fixed scoring rules, its recommendations may not reflect what someone actually enjoys.

Another risk is that the agent could suggest alternative genres or moods that are different from the listener's original preferences.

### Prevention and Safeguards

To reduce these risks, I implemented several safeguards:

- Input validation rejects invalid preferences.
- Recommendation filtering removes songs scoring below 2.0.
- Song scores and explanations make recommendations more transparent.
- The agent preserves the listener's original preferences.
- Agent decisions are recorded in `ai_interactions.md`.
- Automated tests help verify expected behavior.

These safeguards improve reliability and transparency, but they do not guarantee that listeners will enjoy the recommendations.

### Responsible Use

MoodMatch AI is intended for educational purposes, not as a production music recommendation service.

The quality pass rate measures how many songs meet the scoring threshold. It does not measure real listener satisfaction.

## 9. Personal Reflection and AI Collaboration

### What I Learned

Working on this project helped me understand how recommendation systems work and how design decisions affect the results.

In my original Module 3 project, I learned how genre, mood, and energy could be combined into a scoring system.

For Project 4, I learned that generating recommendations is only one part of building a reliable system.

I also needed to validate inputs, filter weak results, evaluate outputs, and test whether the agent's decisions actually improved anything.

### How I Used AI During Development

I used AI assistance, including GitHub Copilot and ChatGPT, to understand Python code, discuss system design, troubleshoot errors, and develop testing ideas.

I did not treat AI-generated suggestions as automatically correct.

I ran the application in VS Code, examined the terminal output, and used pytest to verify that the implementation behaved as expected.

### An AI Suggestion I Accepted

One suggestion I accepted was adding a reliability system to the recommender.

The reliability system validates user preferences and filters songs that score below 2.0.

I accepted this approach because the original system always returned five songs, even when some songs were weak matches.

After implementing the reliability checks, the application returned only songs meeting the threshold.

This made the recommendation criteria more consistent and transparent.

### An AI Suggestion I Revised

During development, the initial agent workflow explored alternative moods when the original playlist was too short.

However, testing showed that changing only the mood did not increase the number of qualifying songs for the pop profile.

Instead of assuming the agent was working correctly simply because the code ran, I checked its actual output.

I revised the workflow to explore both genres and moods.

After the revision, the agent identified an alternative combination with three qualifying songs instead of two.

This taught me that AI suggestions should be evaluated based on observable results, not just whether the code executes successfully.

I also recognized that finding more songs under different preferences does not automatically mean the recommendations are more relevant.

### What Surprised Me

One thing that surprised me in the original project was that changing the scoring weights did not change the top-five rankings for the four profiles.

Another interesting result was Blue Hour Train ranking first for the blues profile despite having a relatively weak energy match.

In Project 4, I was surprised that an agent could execute several decision-making steps and still fail to find an improvement.

That experience showed me why evaluation and testing are important.

### Limitations and Future Improvements

The project still uses a small dataset and fixed scoring rules.

The agent does not measure how closely alternative preferences resemble the listener's original request.

If I continued developing MoodMatch AI, I would:

- Expand the music catalog.
- Add listener feedback and ratings.
- Use additional song attributes.
- Improve alternative recommendations by measuring preference similarity.
- Build an interactive interface.
- Test recommendations with real listeners.

### Final Reflection

Overall, this project helped me understand how coding, AI-assisted development, and testing work together.

I learned that a system should not simply produce an output. It should also explain its decisions, handle invalid inputs, and provide evidence that its behavior matches the intended design.

The biggest lesson I learned is that AI can help me develop ideas and solve problems, but I still need to understand, test, and evaluate the results myself.

## 10. Intended Use and Non-Intended Use

MoodMatch AI is intended for educational demonstrations of recommendation algorithms, reliability checks, and rule-based decision workflows.

It is not intended to replace a commercial music recommendation service or predict listener satisfaction accurately.