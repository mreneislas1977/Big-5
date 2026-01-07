class TeamAnalyzer:
   def __init__(self):
       self.bit_map = {"OPN": 16, "CSN": 8, "EXT": 4, "AGR": 2, "EST": 1}

   def _get_bits(self, profile_id):
       return {
           "OPN": (profile_id & 16) > 0,
           "CSN": (profile_id & 8) > 0,
           "EXT": (profile_id & 4) > 0,
           "AGR": (profile_id & 2) > 0,
           "EST": (profile_id & 1) > 0
       }

   def generate_team_charter(self, team_ids):
       counts = {"OPN": 0, "CSN": 0, "EXT": 0, "AGR": 0, "EST": 0}
       
       for pid in team_ids:
           traits = self._get_bits(pid)
           for key, is_high in traits.items():
               if is_high: counts[key] += 1
       
       principles = []
       dna_tags = []

       # Logic Blocks
       if counts["OPN"] >= 3:
           dna_tags.append("Visionary")
           principles.append({"Rule": "The Kill List", "Why": "Too many ideas.", "Action": "End meetings by cutting ideas."})
       elif counts["OPN"] <= 1:
           dna_tags.append("Pragmatic")
           principles.append({"Rule": "What If Hour", "Why": "Too rigid.", "Action": "Mandatory brainstorming."})

       if counts["CSN"] >= 3:
           dna_tags.append("Disciplined")
           principles.append({"Rule": "Ship It", "Why": "Perfectionism.", "Action": "Strict deadlines."})
       elif counts["CSN"] <= 1:
           dna_tags.append("Agile")
           principles.append({"Rule": "PM Rails", "Why": "Chaos.", "Action": "Hire a Project Manager."})

       if counts["EXT"] >= 3:
           dna_tags.append("High-Energy")
           principles.append({"Rule": "Silent Read", "Why": "Too loud.", "Action": "Read brief before talking."})

       if counts["EST"] <= 1:
           dna_tags.append("Reactive")
           principles.append({"Rule": "24-Hour Rule", "Why": "Panic spirals.", "Action": "No decisions during crisis."})
           
       return {
           "team_fingerprint": dna_tags,
           "operating_principles": principles
       }
