from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ipl_dashboard"]
players = db["players"]
teams   = db["teams"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def seed():
    # ── Real IPL 2024 Teams ─────────────────────────────────────────────────
    if teams.count_documents({}) == 0:
        teams.insert_many([
            {"team": "KKR",  "full_name": "Kolkata Knight Riders",     "wins": 9,  "losses": 4, "points": 18, "matches": 14, "nrr":  1.428},
            {"team": "SRH",  "full_name": "Sunrisers Hyderabad",        "wins": 8,  "losses": 6, "points": 16, "matches": 14, "nrr":  0.416},
            {"team": "RR",   "full_name": "Rajasthan Royals",           "wins": 8,  "losses": 6, "points": 16, "matches": 14, "nrr":  0.273},
            {"team": "CSK",  "full_name": "Chennai Super Kings",        "wins": 7,  "losses": 7, "points": 14, "matches": 14, "nrr":  0.057},
            {"team": "DC",   "full_name": "Delhi Capitals",             "wins": 7,  "losses": 7, "points": 14, "matches": 14, "nrr":  0.074},
            {"team": "MI",   "full_name": "Mumbai Indians",             "wins": 7,  "losses": 7, "points": 14, "matches": 14, "nrr": -0.044},
            {"team": "LSG",  "full_name": "Lucknow Super Giants",       "wins": 7,  "losses": 7, "points": 14, "matches": 14, "nrr": -0.165},
            {"team": "GT",   "full_name": "Gujarat Titans",             "wins": 5,  "losses": 9, "points": 10, "matches": 14, "nrr": -0.230},
            {"team": "RCB",  "full_name": "Royal Challengers Bengaluru","wins": 5,  "losses": 9, "points": 10, "matches": 14, "nrr": -0.408},
            {"team": "PBKS", "full_name": "Punjab Kings",               "wins": 4,  "losses": 10,"points":  8, "matches": 14, "nrr": -1.377},
        ])
        print("Seeded IPL 2024 teams")

    # ── Real IPL 2024 Players (batting + bowling stats) ─────────────────────
    if players.count_documents({}) == 0:
        players.insert_many([
            # Batsmen  – fours & sixes added
            {"name": "Virat Kohli",     "team": "RCB",  "role": "Batsman",      "matches": 15, "runs": 741, "avg": 61.75, "sr": 154.69, "fours": 72, "sixes": 20, "wickets": 0, "economy": 0.0},
            {"name": "Travis Head",     "team": "SRH",  "role": "Batsman",      "matches": 15, "runs": 567, "avg": 40.50, "sr": 191.55, "fours": 48, "sixes": 34, "wickets": 0, "economy": 0.0},
            {"name": "Abhishek Sharma", "team": "SRH",  "role": "Batsman",      "matches": 14, "runs": 484, "avg": 34.57, "sr": 198.36, "fours": 38, "sixes": 32, "wickets": 0, "economy": 0.0},
            {"name": "Sai Sudharsan",   "team": "GT",   "role": "Batsman",      "matches": 14, "runs": 527, "avg": 43.91, "sr": 139.68, "fours": 58, "sixes": 12, "wickets": 0, "economy": 0.0},
            {"name": "Riyan Parag",     "team": "RR",   "role": "Batsman",      "matches": 14, "runs": 573, "avg": 52.09, "sr": 149.60, "fours": 55, "sixes": 22, "wickets": 0, "economy": 0.0},
            {"name": "Shubman Gill",    "team": "GT",   "role": "Batsman",      "matches": 14, "runs": 426, "avg": 35.50, "sr": 139.47, "fours": 43, "sixes": 14, "wickets": 0, "economy": 0.0},
            {"name": "Rohit Sharma",    "team": "MI",   "role": "Batsman",      "matches": 14, "runs": 417, "avg": 29.78, "sr": 141.01, "fours": 40, "sixes": 18, "wickets": 0, "economy": 0.0},
            {"name": "Ruturaj Gaikwad", "team": "CSK",  "role": "Batsman",      "matches": 14, "runs": 583, "avg": 44.84, "sr": 145.00, "fours": 60, "sixes": 16, "wickets": 0, "economy": 0.0},

            # Wicket-keepers
            {"name": "KL Rahul",        "team": "LSG",  "role": "Wicket-keeper","matches": 14, "runs": 520, "avg": 43.33, "sr": 136.12, "fours": 50, "sixes": 14, "wickets": 0, "economy": 0.0},
            {"name": "Quinton de Kock", "team": "KKR",  "role": "Wicket-keeper","matches": 14, "runs": 391, "avg": 29.92, "sr": 155.55, "fours": 36, "sixes": 20, "wickets": 0, "economy": 0.0},
            {"name": "MS Dhoni",        "team": "CSK",  "role": "Wicket-keeper","matches": 14, "runs": 161, "avg": 53.66, "sr": 220.54, "fours":  8, "sixes": 18, "wickets": 0, "economy": 0.0},
            {"name": "Sanju Samson",    "team": "RR",   "role": "Wicket-keeper","matches": 13, "runs": 531, "avg": 48.27, "sr": 153.46, "fours": 46, "sixes": 26, "wickets": 0, "economy": 0.0},

            # All-rounders
            {"name": "Hardik Pandya",   "team": "MI",   "role": "All-rounder",  "matches": 14, "runs": 216, "avg": 18.00, "sr": 139.35, "fours": 18, "sixes": 14, "wickets": 11, "economy": 9.40},
            {"name": "Andre Russell",   "team": "KKR",  "role": "All-rounder",  "matches": 14, "runs": 222, "avg": 27.75, "sr": 187.34, "fours": 14, "sixes": 22, "wickets": 19, "economy": 9.87},
            {"name": "Ravindra Jadeja", "team": "CSK",  "role": "All-rounder",  "matches": 14, "runs": 169, "avg": 28.16, "sr": 156.48, "fours": 12, "sixes":  8, "wickets": 19, "economy": 7.84},
            {"name": "Axar Patel",      "team": "DC",   "role": "All-rounder",  "matches": 14, "runs": 175, "avg": 25.00, "sr": 157.65, "fours": 14, "sixes": 10, "wickets": 14, "economy": 8.02},
            {"name": "Sunil Narine",    "team": "KKR",  "role": "All-rounder",  "matches": 14, "runs": 488, "avg": 48.80, "sr": 178.83, "fours": 44, "sixes": 28, "wickets": 17, "economy": 6.74},

            # Bowlers  – economy & wickets added
            {"name": "Jasprit Bumrah",  "team": "MI",   "role": "Bowler",       "matches": 13, "runs": 11,  "avg": 5.50,  "sr": 78.57,  "fours":  0, "sixes":  0, "wickets": 15, "economy": 6.48},
            {"name": "Harshal Patel",   "team": "RCB",  "role": "Bowler",       "matches": 14, "runs":  5,  "avg": 2.50,  "sr": 50.00,  "fours":  0, "sixes":  0, "wickets": 13, "economy": 9.22},
            {"name": "Mohammed Siraj",  "team": "RCB",  "role": "Bowler",       "matches": 14, "runs":  8,  "avg": 4.00,  "sr": 57.14,  "fours":  0, "sixes":  0, "wickets": 14, "economy": 9.54},
            {"name": "T Natarajan",     "team": "SRH",  "role": "Bowler",       "matches": 14, "runs": 10,  "avg": 5.00,  "sr": 62.50,  "fours":  0, "sixes":  0, "wickets": 19, "economy": 9.12},
            {"name": "Rashid Khan",     "team": "GT",   "role": "Bowler",       "matches": 14, "runs": 88,  "avg": 14.66, "sr": 142.85, "fours":  4, "sixes":  8, "wickets": 17, "economy": 8.24},
        ])
        print("Seeded IPL 2024 players")

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/overview")
def overview():
    top = players.find_one(sort=[("runs", -1)])
    pts = list(teams.find({}, {"_id": 0}).sort("points", -1))
    top5 = list(players.find({}, {"_id": 0, "name": 1, "team": 1, "runs": 1}).sort("runs", -1).limit(5))
    return jsonify({
        "total_teams":   teams.count_documents({}),
        "total_players": players.count_documents({}),
        "total_matches": sum(t["matches"] for t in teams.find()) // 2,
        "top_score":     f"{top['runs']} runs" if top else "—",
        "points_table":  pts,
        "top_scorers":   top5,
    })

@app.route("/api/players", methods=["GET"])
def get_players():
    role   = request.args.get("role", "")
    query  = {"role": role} if role else {}
    return jsonify([fix_id(p) for p in players.find(query)])

@app.route("/api/players", methods=["POST"])
def add_player():
    data = request.json
    # Ensure new fields exist
    data.setdefault("fours",   0)
    data.setdefault("sixes",   0)
    data.setdefault("wickets", 0)
    data.setdefault("economy", 0.0)
    result = players.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route("/api/players/<pid>", methods=["PUT"])
def update_player(pid):
    players.update_one({"_id": ObjectId(pid)}, {"$set": request.json})
    return jsonify({"message": "updated"})

@app.route("/api/players/<pid>", methods=["DELETE"])
def delete_player(pid):
    players.delete_one({"_id": ObjectId(pid)})
    return jsonify({"message": "deleted"})

@app.route("/api/leaderboard")
def leaderboard():
    top = list(players.find({}, {"_id": 0}).sort("runs", -1).limit(10))
    return jsonify(top)

@app.route("/api/winrate")
def winrate():
    pipeline = [
        {"$addFields": {"win_pct": {"$multiply": [{"$divide": ["$wins", {"$add": ["$wins", "$losses"]}]}, 100]}}},
        {"$project": {"_id": 0, "team": 1, "wins": 1, "losses": 1, "win_pct": 1}},
        {"$sort": {"win_pct": -1}}
    ]
    return jsonify(list(teams.aggregate(pipeline)))

if __name__ == "__main__":
    seed()
    app.run(debug=True, port=5000)