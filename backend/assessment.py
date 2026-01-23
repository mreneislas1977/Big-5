import json
import os

def calculate_big5_scores(answers):
    """
    Calculates the average score (1-5) for each of the Big 5 traits.
    Expects 'answers' to be a dict like {'q1': 5, 'q2': 3, ...}
    """
    # 1. Load Question Data to know which question belongs to which trait
    # We try to load from the file, or fall back to defaults if missing.
    try:
        path = os.path.join(os.getcwd(), 'data', 'questions.json')
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading questions for scoring: {e}")
        return {"error": "scoring_config_missing"}

    # 2. Initialize scores
    scores = {
        "openness": [],
        "conscientiousness": [],
        "extraversion": [],
        "agreeableness": [],
        "stability": []
    }

    # 3. Map answers to categories
    # The JSON structure is [{"id": "openness", "questions": [...]}, ...]
    for category in data:
        trait_id = category["id"] # e.g. "openness"
        for q in category["questions"]:
            qid = q["id"] # e.g. "q1"
            if qid in answers:
                try:
                    val = int(answers[qid])
                    scores[trait_id].append(val)
                except ValueError:
                    continue # Skip invalid inputs
    
    # 4. Calculate Averages
    final_scores = {}
    for trait, values in scores.items():
        if len(values) > 0:
            final_scores[trait] = round(sum(values) / len(values), 2)
        else:
            final_scores[trait] = 0 # Default if no questions answered for this trait

    return final_scores

def determine_archetype(scores, profiles):
    """
    Matches the calculated scores against the profiles.json to find the best fit.
    """
    best_match = None
    min_diff = float('inf')

    # If scores is invalid (empty), return default
    if not scores or "error" in scores:
        return {
            "archetype": "Assessment Incomplete",
            "description": "We could not generate a valid score from your answers.",
            "recommendation": "Please try taking the assessment again."
        }

    for profile in profiles:
        # Calculate total difference between user scores and this profile's ideal scores
        # We assume standard Euclidean distance or simple absolute difference
        diff = 0
        profile_scores = profile.get("scores", {})
        
        for trait, value in scores.items():
            # Get the profile's expected value for this trait (default to 3 if missing)
            target = profile_scores.get(trait, 3) 
            diff += abs(value - target)
        
        if diff < min_diff:
            min_diff = diff
            best_match = profile

    if best_match:
        return {
            "archetype": best_match["name"],
            "description": best_match["description"],
            "recommendation": best_match["recommendation"],
            "scores": scores
        }
    
    return {
        "archetype": "The Generalist",
        "description": "Your leadership style is balanced across all traits.",
        "recommendation": "Focus on adapting your style to the specific needs of your team.",
        "scores": scores
    }
