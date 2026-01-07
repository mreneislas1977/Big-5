import json
import os

class BigFiveAssessment:
   def __init__(self):
       current_dir = os.path.dirname(__file__)
       with open(os.path.join(current_dir, '../data/profiles.json'), 'r') as f:
           self.profiles = json.load(f)

       # + is standard, - is reverse scored
       self.scoring_key = {
           "EXT": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
           "EST": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
           "AGR": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
           "CSN": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
           "OPN": {"+": [1, 3, 5, 7, 9], "-": [2, 4, 6, 8, 10]}, 
       }
       
       self.bit_map = {"OPN": 16, "CSN": 8, "EXT": 4, "AGR": 2, "EST": 1}

   def calculate_score(self, trait, user_responses):
       score = 0
       for q_id in self.scoring_key[trait]["+"]:
           score += user_responses.get(f"{trait}_{q_id}", 3)
       for q_id in self.scoring_key[trait]["-"]:
           val = user_responses.get(f"{trait}_{q_id}", 3)
           score += (6 - val)
       return round(((score - 10) / 40) * 100, 1)

   def generate_full_report(self, user_responses):
       scores = {}
       profile_id = 0
       
       for trait in ["EXT", "EST", "AGR", "CSN", "OPN"]:
           val = self.calculate_score(trait, user_responses)
           scores[trait] = val
           if val > 50:
               profile_id += self.bit_map[trait]

       profile_data = self.profiles.get(str(profile_id), {})

       return {
           "scores": scores,
           "profile_id": profile_id,
           "archetype": profile_data.get("name", "Unknown"),
           "description": profile_data.get("description", ""),
           "recommendation": profile_data.get("happiness_tip", "")
       }
