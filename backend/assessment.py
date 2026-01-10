import json
import os

class BigFiveAssessment:
    def __init__(self):
        # 1. Define Logic FIRST (so the app can run even without data)
        # + is standard, - is reverse scored
        self.scoring_key = {
            "EXT": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
            "EST": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
            "AGR": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
            "CSN": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
            "OPN": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
        }
        self.bit_map = {"OPN": 16, "CSN": 8, "EXT": 4, "AGR": 2, "EST": 1}
        self.profiles = {}

        # 2. Try to load Data SAFELY
        try:
            current_dir = os.path.dirname(__file__)
            # Construct path to ../data/profiles.json
            data_path = os.path.join(current_dir, '../data/profiles.json')
            
            if os.path.exists(data_path):
                with open(data_path, 'r') as f:
                    self.profiles = json.load(f)
                print(f"SUCCESS: Loaded {len(self.profiles)} profiles.")
            else:
                print(f"WARNING: profiles.json not found at {data_path}. Using empty profiles.")
                
        except Exception as e:
            # If this fails, we DO NOT CRASH. We just print the error.
            print(f"ERROR loading profiles: {e}")
            self.profiles = {}

    def calculate_score(self, trait, user_responses):
        score = 0
        try:
            for q_id in self.scoring_key[trait]["+"]:
                score += user_responses.get(f"{trait}_{q_id}", 3)
            for q_id in self.scoring_key[trait]["-"]:
                val = user_responses.get(f"{trait}_{q_id}", 3)
                score += (6 - val)
            return round(((score - 10) / 40) * 100, 1)
        except Exception as e:
            print(f"Math Error on {trait}: {e}")
            return 50.0  # Return average score on failure

    def generate_full_report(self, user_responses):
        scores = {}
        profile_id = 0
        
        # Calculate Scores
        for trait in ["EXT", "EST", "AGR", "CSN", "OPN"]:
            val = self.calculate_score(trait, user_responses)
            scores[trait] = val
            if val > 50:
                profile_id += self.bit_map[trait]

        # Get Profile (Safe .get method prevents crash)
        profile_data = self.profiles.get(str(profile_id), {})

        return {
            "scores": scores,
            "profile_id": profile_id,
            "archetype": profile_data.get("name", "Unknown Archetype (Data Missing)"),
            "description": profile_data.get("description", "Could not load profile description."),
            "recommendation": profile_data.get("happiness_tip", "No recommendation available.")
        }
