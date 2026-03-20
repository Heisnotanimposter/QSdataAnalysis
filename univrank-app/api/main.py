from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
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
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
