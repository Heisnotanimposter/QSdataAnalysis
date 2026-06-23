from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/rankings')
def get_rankings():
    try:
        # Load CSV data
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'world_university_rankings_2026.csv')
        df = pd.read_csv(csv_path)
        
        # Convert to the format expected by the frontend
        rankings = []
        for _, row in df.iterrows():
            def to_int(val):
                try:
                    return int(float(val)) if pd.notna(val) else None
                except:
                    return None
                
            def to_float(val):
                try:
                    return float(val) if pd.notna(val) else 0.0
                except:
                    return 0.0

            def to_float_or_none(val):
                try:
                    return float(val) if pd.notna(val) else None
                except:
                    return None
            
            # Determine tuition fee range
            tuition = "40,000 - 60,000 USD" if row.get('university_type') == 'Private' else "5,000 - 15,000 USD"
            
            university = {
                "university_id": f"U{row.name + 1:03d}",
                "university_name": row['university'],
                "country": row['country'],
                "region": row['region'],
                "university_type": row['university_type'] if pd.notna(row['university_type']) else 'Public',
                "subject_area": ["General"],
                "qs_rank": to_int(row.get('qs_rank_2026')),
                "the_rank": to_int(row.get('the_rank_2026')),
                "arwu_rank": to_int(row.get('arwu_rank_2025')),
                "scimago_rank": None,
                "webometrics_rank": None,
                "studyportals_rank": None,
                "uniranks_rank": None,
                "qs_stars": "5 Stars" if to_int(row.get('qs_rank_2026')) and to_int(row.get('qs_rank_2026')) <= 50 else "4 Stars",
                "sustainability_score": to_float(row.get('qs_score')),
                "research_impact_score": to_float(row.get('qs_citations')),
                "employer_reputation_score": to_float(row.get('qs_employer_rep')),
                "faculty_student_ratio": to_float(row.get('qs_faculty_student')),
                "international_outlook_score": to_float(row.get('the_intl_outlook')),
                "teaching_quality_score": to_float(row.get('the_teaching')),
                "founding_year": to_int(row.get('founded')),
                "student_population": to_int(row.get('total_students')),
                "international_student_percentage": to_float_or_none(row.get('intl_students_pct')),
                "nobel_laureates": to_int(row.get('nobel_laureates')),
                "tuition_fee_range": tuition,
                "programs_offered": ["BSc", "MSc", "PhD"],
                "website_url": f"https://www.{str(row['university']).lower().replace(' ', '').replace(',', '').replace('.', '')}.edu",
                "univrank": 0  # Will be calculated by frontend
            }
            rankings.append(university)
        
        return jsonify(rankings)
    
    except FileNotFoundError as e:
        print(f"CSV file not found: {e}")
        # Fallback to JSON data if CSV fails
        json_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'rankings.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        else:
            return jsonify({"error": "No data available"}), 500
    except pd.errors.EmptyDataError as e:
        print(f"CSV file is empty: {e}")
        return jsonify({"error": "Data file is empty"}), 500
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting UNIVrank API server...")
    print("Available endpoints:")
    print("  GET /rankings - University rankings data")
    print("  GET /health - Health check")
    app.run(debug=True, port=8000)
