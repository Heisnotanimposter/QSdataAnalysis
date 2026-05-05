import json
import os

the_data = [
  {"name": "University of Oxford", "the_rank": "1", "country": "United Kingdom"},
  {"name": "Massachusetts Institute of Technology", "the_rank": "2", "country": "United States"},
  {"name": "Harvard University", "the_rank": "3", "country": "United States"},
  {"name": "Princeton University", "the_rank": "4", "country": "United States"},
  {"name": "University of Cambridge", "the_rank": "5", "country": "United Kingdom"},
  {"name": "Stanford University", "the_rank": "6", "country": "United States"},
  {"name": "California Institute of Technology", "the_rank": "7", "country": "United States"},
  {"name": "University of California, Berkeley", "the_rank": "8", "country": "United States"},
  {"name": "Imperial College London", "the_rank": "9", "country": "United Kingdom"},
  {"name": "Yale University", "the_rank": "10", "country": "United States"},
  {"name": "ETH Zurich", "the_rank": "11", "country": "Switzerland"},
  {"name": "Tsinghua University", "the_rank": "12", "country": "China"},
  {"name": "Peking University", "the_rank": "13", "country": "China"},
  {"name": "The University of Chicago", "the_rank": "14", "country": "United States"},
  {"name": "University of Pennsylvania", "the_rank": "14", "country": "United States"},
  {"name": "Johns Hopkins University", "the_rank": "16", "country": "United States"},
  {"name": "National University of Singapore", "the_rank": "17", "country": "Singapore"},
  {"name": "Columbia University", "the_rank": "18", "country": "United States"},
  {"name": "University of California, Los Angeles", "the_rank": "18", "country": "United States"},
  {"name": "Cornell University", "the_rank": "20", "country": "United States"},
  {"name": "University of Toronto", "the_rank": "21", "country": "Canada"},
  {"name": "UCL", "the_rank": "22", "country": "United Kingdom"},
  {"name": "University of Michigan-Ann Arbor", "the_rank": "22", "country": "United States"},
  {"name": "Carnegie Mellon University", "the_rank": "24", "country": "United States"},
  {"name": "University of Washington", "the_rank": "25", "country": "United States"},
  {"name": "Technical University of Munich", "the_rank": "26", "country": "Germany"},
  {"name": "Duke University", "the_rank": "27", "country": "United States"},
  {"name": "The University of Tokyo", "the_rank": "28", "country": "Japan"},
  {"name": "University of Edinburgh", "the_rank": "29", "country": "United Kingdom"},
  {"name": "Nanyang Technological University, Singapore", "the_rank": "30", "country": "Singapore"},
  {"name": "Northwestern University", "the_rank": "31", "country": "United States"},
  {"name": "École Polytechnique Fédérale de Lausanne", "the_rank": "32", "country": "Switzerland"},
  {"name": "New York University", "the_rank": "33", "country": "United States"},
  {"name": "University of California, San Diego", "the_rank": "34", "country": "United States"},
  {"name": "University of Hong Kong", "the_rank": "35", "country": "Hong Kong"},
  {"name": "Fudan University", "the_rank": "36", "country": "China"},
  {"name": "King’s College London", "the_rank": "36", "country": "United Kingdom"},
  {"name": "LMU Munich", "the_rank": "38", "country": "Germany"},
  {"name": "University of Melbourne", "the_rank": "39", "country": "Australia"},
  {"name": "Georgia Institute of Technology", "the_rank": "40", "country": "United States"},
  {"name": "University of British Columbia", "the_rank": "41", "country": "Canada"},
  {"name": "PSL Research University", "the_rank": "42", "country": "France"},
  {"name": "KU Leuven", "the_rank": "43", "country": "Belgium"},
  {"name": "The Chinese University of Hong Kong", "the_rank": "44", "country": "Hong Kong"},
  {"name": "McGill University", "the_rank": "45", "country": "Canada"},
  {"name": "University of Illinois at Urbana-Champaign", "the_rank": "46", "country": "United States"},
  {"name": "Universität Heidelberg", "the_rank": "47", "country": "Germany"},
  {"name": "Zhejiang University", "the_rank": "47", "country": "China"},
  {"name": "Karolinska Institute", "the_rank": "49", "country": "Sweden"},
  {"name": "London School of Economics and Political Science", "the_rank": "50", "country": "United Kingdom"},
  {"name": "University of Texas at Austin", "the_rank": "50", "country": "United States"}
]

output_path = '/Users/seungwonlee/QSdataAnalysis/univrank-app/src/data/rankings.json'
with open(output_path, 'r') as f:
    existing_data = json.load(f)

lookup = {u['university_name'].lower().replace('univ of', 'university of'): u for u in existing_data}

# Handle fuzzy matching for common names
fuzzy_map = {
    "mit": "massachusetts institute of technology",
    "ucl": "university college london",
    "eth zurich": "eth zurich",
    "technical university of munich": "technical univ of munich",
    "lmu munich": "lmu munich",
    "psl research university": "psl university",
    "university of oxford": "oxford",
    "university of cambridge": "cambridge",
}

updates = 0
for entry in the_data:
    name = entry['name'].lower()
    rank = int(entry['the_rank'].replace('=', ''))
    
    # Try fuzzy or direct match
    target_name = name
    if name in fuzzy_map:
        target_name = fuzzy_map[name]
    
    found = False
    for ex_name, u in lookup.items():
        if target_name in ex_name or ex_name in target_name:
            u['the_rank'] = rank
            updates += 1
            found = True
            break
            
print(f"Merged {updates} THE records into rankings.json")

with open(output_path, 'w') as f:
    json.dump(existing_data, f, indent=2)
