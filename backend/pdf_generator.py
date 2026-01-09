import os
import numpy as np
import matplotlib
matplotlib.use('Agg') # <--- CRITICAL FIX FOR DOCKER
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
   def header(self):
       self.set_font('Helvetica', 'B', 10)
       self.set_text_color(128)
       self.cell(0, 10, 'Personality Assessment', 0, 1, 'R')
       self.ln(5)

def create_radar_chart(scores, filename="temp_chart.png"):
   labels = list(scores.keys())
   stats = list(scores.values())
   stats += [stats[0]]
   angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
   angles += [angles[0]]

   fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
   ax.plot(angles, stats, color='#36A2EB', linewidth=2)
   ax.fill(angles, stats, color='#36A2EB', alpha=0.25)
   ax.set_ylim(0, 100)
   ax.set_yticklabels([])
   ax.set_xticks(angles[:-1])
   ax.set_xticklabels(labels)
   plt.tight_layout()
   plt.savefig(filename)
   plt.close()

def generate_pdf(user_name, profile_data, filename="Report.pdf"):
   pdf = PDFReport()
   pdf.add_page()
   
   pdf.set_font('Helvetica', 'B', 24)
   pdf.cell(0, 20, f"Profile: {user_name}", 0, 1, 'C')
   
   pdf.set_font('Helvetica', 'B', 16)
   pdf.cell(0, 10, f"Archetype: {profile_data['archetype']}", 0, 1, 'C')
   
   create_radar_chart(profile_data['scores'], "chart.png")
   pdf.image("chart.png", x=55, w=100)
   
   pdf.ln(5)
   pdf.set_font('Helvetica', '', 12)
   pdf.multi_cell(0, 6, profile_data['description'])
   
   pdf.ln(5)
   pdf.set_font('Helvetica', 'B', 12)
   pdf.set_text_color(0, 100, 0)
   pdf.cell(0, 10, "Recommendation:", 0, 1)
   
   pdf.set_font('Helvetica', 'I', 12)
   pdf.set_text_color(50)
   pdf.multi_cell(0, 6, profile_data['recommendation'])

   pdf.output(filename)
   if os.path.exists("chart.png"): os.remove("chart.png")
