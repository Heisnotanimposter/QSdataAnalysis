from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import pandas as pd
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="UnivAPI", description="API for University Rankings and Insights")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../src/data/rankings.json")
CSV_PATH = os.path.join(os.path.dirname(__file__), "../../world_university_rankings_2026.csv")

class University(BaseModel):
    university_id: str
    university_name: str
    country: str
    region: str
    univrank: int
    qs_rank: Optional[int]
    the_rank: Optional[int]
    arwu_rank: Optional[int]
    sustainability_score: float
    research_impact_score: float
    student_population: Optional[int]
    tuition_fee_range: str
    website_url: str

def load_data():
    # Try to load CSV data first
    try:
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            rankings = []
            for _, row in df.iterrows():
                university = {
                    "university_id": f"U{row.name + 1:03d}",
                    "university_name": row['university'],
                    "country": row['country'],
                    "region": row['region'],
                    "university_type": row['university_type'],
                    "qs_rank": int(row['qs_rank_2026']) if pd.notna(row['qs_rank_2026']) else None,
                    "the_rank": int(row['the_rank_2026']) if pd.notna(row['the_rank_2026']) else None,
                    "arwu_rank": int(row['arwu_rank_2025']) if pd.notna(row['arwu_rank_2025']) else None,
                    "sustainability_score": float(row['qs_intl_students']) if pd.notna(row['qs_intl_students']) else 0.0,
                    "research_impact_score": float(row['qs_citations']) if pd.notna(row['qs_citations']) else 0.0,
                    "student_population": int(row['total_students']) if pd.notna(row['total_students']) else 0,
                    "tuition_fee_range": "Varies by institution",
                    "website_url": f"https://www.{row['university'].lower().replace(' ', '').replace(',', '').replace('.', '')}.edu",
                    "univrank": 0  # Will be calculated by frontend
                }
                rankings.append(university)
            return rankings
    except Exception as e:
        print(f"Error loading CSV: {e}")
    
    # Fallback to JSON data
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return []

@app.get("/rankings", response_model=List[dict])
async def get_rankings():
    return load_data()

@app.get("/university/{univ_id}")
async def get_university(univ_id: str):
    data = load_data()
    for u in data:
        if u["university_id"] == univ_id:
            return u
    raise HTTPException(status_code=404, detail="University not found")

@app.get("/stats")
async def get_stats():
    data = load_data()
    return {
        "total_universities": len(data),
        "regions": list(set(u["region"] for u in data)),
        "countries": list(set(u["country"] for u in data))
    }

@app.post("/evaluate")
async def evaluate_applicant(applicant_data: dict):
    """Evaluate applicant against target university"""
    try:
        data = load_data()
        target_university = applicant_data.get("target_university")
        applicant_gpa = applicant_data.get("gpa", 0.0)
        test_scores = applicant_data.get("test_scores", {})
        
        # Find target university data
        target_data = None
        for uni in data:
            if uni.get("university_name") == target_university:
                target_data = uni
                break
        
        if not target_data:
            raise HTTPException(status_code=404, detail="Target university not found")
        
        # Calculate acceptance probability (simplified algorithm)
        target_rank = target_data.get("qs_rank", 100)
        
        # Factors affecting admission
        gpa_score = (applicant_gpa / 4.0) * 30  # 30% weight
        gre_score = ((test_scores.get("gre", 150) - 150) / 40) * 20  # 20% weight
        toefl_score = ((test_scores.get("toefl", 90) - 90) / 30) * 15  # 15% weight
        rank_factor = max(0, (100 - target_rank) / 100) * 20  # 20% weight
        random_factor = 15  # 15% for other factors
        
        acceptance_probability = min(95, max(5, 
            gpa_score + gre_score + toefl_score + rank_factor + random_factor
        ))
        
        # Generate recommendations
        recommendations = []
        if acceptance_probability < 70:
            recommendations.append("Strengthen Statement of Purpose")
        if applicant_gpa < 3.7:
            recommendations.append("Improve academic performance")
        if test_scores.get("gre", 0) < 165:
            recommendations.append("Retake GRE for better score")
        
        # Identify gaps
        gaps = []
        if applicant_gpa < 3.5:
            gaps.append("GPA below competitive threshold")
        if test_scores.get("gre", 0) < 160:
            gaps.append("GRE score could be improved")
        
        return {
            "acceptance_probability": round(acceptance_probability),
            "academics": "A" if acceptance_probability > 70 else "B" if acceptance_probability > 50 else "C",
            "gpa_converted": applicant_gpa,
            "coursework_status": "Passed" if acceptance_probability > 60 else "Needs Improvement",
            "gaps": gaps,
            "recommendations": recommendations,
            "target_profile": {
                "name": target_university,
                "rank": target_rank,
                "region": target_data.get("region"),
                "type": target_data.get("university_type")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
