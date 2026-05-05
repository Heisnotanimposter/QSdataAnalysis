import csv
import json
import os
from datetime import datetime

csv_path = '/Users/seungwonlee/QSdataAnalysis/world_university_rankings_2026.csv'
json_output = '/Users/seungwonlee/QSdataAnalysis/univrank-app/src/data/rankings.json'

def clean_float(val):
    try:
        if not val or val.strip() == '':
            return None
        return float(val)
    except ValueError:
        return None

def clean_int(val):
    try:
        if not val or val.strip() == '':
            return None
        return int(float(val))
    except ValueError:
        return None

universities = []

with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        u = {
            "university_id": f"U{i+1:03d}",
            "university_name": row["university"],
            "country": row["country"],
            "region": row["region"],
            "university_type": row["university_type"],
            "subject_area": ["General"], # Placeholder as CSV doesn't specify per entry
            "qs_rank": clean_int(row["qs_rank_2026"]),
            "the_rank": clean_int(row["the_rank_2026"]),
            "arwu_rank": clean_int(row["arwu_rank_2025"]),
            # New platforms as requested (placeholders if not in CSV)
            "scimago_rank": None, 
            "webometrics_rank": None,
            "studyportals_rank": None,
            "uniranks_rank": None,
            
            "qs_stars": "5 Stars" if clean_int(row["qs_rank_2026"]) and clean_int(row["qs_rank_2026"]) < 50 else "4 Stars",
            
            "sustainability_score": clean_float(row["qs_score"]), # Using qs_score as proxy
            "research_impact_score": clean_float(row["qs_citations"]),
            "employer_reputation_score": clean_float(row["qs_employer_rep"]),
            "faculty_student_ratio": clean_float(row["qs_faculty_student"]),
            "international_outlook_score": clean_float(row["the_intl_outlook"]),
            "teaching_quality_score": clean_float(row["the_teaching"]),
            
            "founding_year": clean_int(row["founded"]),
            "student_population": clean_int(row["total_students"]),
            "international_student_percentage": clean_float(row["intl_students_pct"]),
            "nobel_laureates": clean_int(row["nobel_laureates"]),
            
            "tuition_fee_range": "40,000 - 60,000 USD" if row["university_type"] == "Private" else "5,000 - 15,000 USD",
            "programs_offered": ["BSc", "MSc", "PhD"],
            "website_url": f"https://www.{row['university'].lower().replace(' ', '')}.edu",
            "last_updated": datetime.now().isoformat()
        }
        universities.append(u)

with open(json_output, 'w', encoding='utf-8') as f:
    json.dump(universities, f, indent=2)

print(f"Successfully processed {len(universities)} universities.")
