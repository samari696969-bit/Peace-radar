from flask import Flask, jsonify, render_template
from database import init_db, get_events, get_region_status

app = Flask(__name__)
init_db()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/events")
def events():
    return jsonify(get_events(limit=100))

@app.get("/api/status")
def status():
    return jsonify(get_region_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").getenv("PORT", 5000)))
