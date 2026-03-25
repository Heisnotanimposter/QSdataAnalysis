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
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'world_university_rankings_2026.csv')
        df = pd.read_csv(csv_path)
        
        # Convert to the format expected by the frontend
        rankings = []
        for _, row in df.iterrows():
            university = {
                "university_id": f"U{row.name + 1:03d}",
                "university_name": row['university'],
                "country": row['country'],
                "region": row['region'],
                "university_type": row['university_type'],
                "subject_area": ["General"],
                "qs_rank": int(row['qs_rank_2026']) if pd.notna(row['qs_rank_2026']) else None,
                "the_rank": int(row['the_rank_2026']) if pd.notna(row['the_rank_2026']) else None,
                "arwu_rank": int(row['arwu_rank_2025']) if pd.notna(row['arwu_rank_2025']) else None,
                "scimago_rank": None,
                "webometrics_rank": None,
                "studyportals_rank": None,
                "uniranks_rank": None,
                "qs_stars": "5 Stars",
                "sustainability_score": float(row['qs_intl_students']) if pd.notna(row['qs_intl_students']) else 0.0,
                "research_impact_score": float(row['qs_citations']) if pd.notna(row['qs_citations']) else 0.0,
                "employer_reputation_score": float(row['qs_employer_rep']) if pd.notna(row['qs_employer_rep']) else 0.0,
                "faculty_student_ratio": float(row['qs_faculty_student']) if pd.notna(row['qs_faculty_student']) else 0.0,
                "international_outlook_score": float(row['qs_intl_faculty']) if pd.notna(row['qs_intl_faculty']) else 0.0,
                "teaching_quality_score": float(row['the_teaching']) if pd.notna(row['the_teaching']) else 0.0,
                "founding_year": int(row['founded']) if pd.notna(row['founded']) else 1800,
                "student_population": int(row['total_students']) if pd.notna(row['total_students']) else 0,
                "international_student_percentage": float(row['intl_students_pct']) if pd.notna(row['intl_students_pct']) else 0.0,
                "nobel_laureates": int(row['nobel_laureates']) if pd.notna(row['nobel_laureates']) else 0,
                "tuition_fee_range": "Varies by institution",
                "programs_offered": ["Various"],
                "website_url": f"https://www.{row['university'].lower().replace(' ', '').replace(',', '').replace('.', '')}.edu",
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
