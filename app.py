from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# =========================
# LOAD DATASET
# =========================
def load_keywords():
    rules = []
    with open("scam_keywords.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rules.append(row)
    return rules

SCAM_DATASET = load_keywords()

# =========================
# MAIN PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    risk = ""
    trust_score = 0
    reasons = []
    suggestions = []

    if request.method == "POST":
        text = request.form.get("description", "").lower()

        score = 0
        for item in SCAM_DATASET:
            if item["keyword"].lower() in text:
                score += int(item["score"])
                reasons.append(item["reason"])

        score = min(score, 100)
        trust_score = 100 - score

        if trust_score < 40:
            risk = "High Risk Internship 🔴"
            suggestions = [
                "Never pay any registration or joining fee",
                "Avoid WhatsApp-only communication",
                "Verify company on official website"
            ]
        elif trust_score < 70:
            risk = "Medium Risk Internship 🟠"
            suggestions = [
                "Verify offer letter and email ID",
                "Consult seniors or T&P cell"
            ]
        else:
            risk = "Low Risk Internship 🟢"
            suggestions = [
                "Looks safe, but stay alert",
                "Never share OTP or documents"
            ]

    return render_template(
        "index.html",
        risk=risk,
        trust_score=trust_score,
        reasons=reasons,
        suggestions=suggestions
    )

# =========================
# CHATBOT API
# =========================
@app.route("/chatbot", methods=["POST"])
def chatbot():
    msg = request.form.get("message", "").lower()

    for item in SCAM_DATASET:
        if item["keyword"].lower() in msg:
            return f"⚠️ Warning: {item['reason']}"

    return "ℹ️ Always verify internships on official websites and never pay fees."

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
