from flask import Flask, request, render_template
import csv
import random
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "oscars.csv")

# Easy categories
EASY_CATEGORIES = [
    "ACTOR IN A LEADING ROLE",
    "ACTRESS IN A LEADING ROLE",
    "BEST PICTURE",
    "DIRECTING",
    "DIRECTING (Dramatic Picture)",
    "DIRECTING (Comedy Picture)"
]

# Load winners from CSV
def load_winners():
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row["winner"].lower() == "true"]

ALL_WINNERS = load_winners()
EASY_WINNERS = [row for row in ALL_WINNERS if row["canon_category"] in EASY_CATEGORIES]

def format_category(category):
    if "DIRECTING" in category:
        return "BEST DIRECTOR"
    if category == "ACTOR IN A LEADING ROLE":
        return "BEST ACTOR"
    if category == "ACTRESS IN A LEADING ROLE":
        return "BEST ACTRESS"
    return category

@app.route("/", methods=["GET", "POST"])
def quiz():
    mode = request.args.get("mode", "easy")
    if mode == "hard":
        winners = ALL_WINNERS
        toggle_mode = "easy"
        toggle_label = "Switch to Easy Mode"
    else:
        winners = EASY_WINNERS
        toggle_mode = "hard"
        toggle_label = "Switch to Hard Mode"

    if request.method == "POST":
        correct_answer = request.form.get("correct_answer", "")
        category = request.form.get("category", "")
        year = request.form.get("year", "")
        film = request.form.get("film", "")
        mode = request.form.get("mode", mode)
        user_answer = request.form.get("answer", "")

        if user_answer.strip().lower() in correct_answer.lower():
            result = f"✅ Correct! {correct_answer} won for '{film}'."
        else:
            result = f"❌ Incorrect. Correct answer: {correct_answer} (won for '{film}')"

        return render_template("quiz.html",
                               mode=mode,
                               toggle_mode=toggle_mode,
                               toggle_label=toggle_label,
                               question=f"Who won {category} in {year}?",
                               result=result,
                               show_next=True)

    # GET: new question
    row = random.choice(winners)
    category = format_category(row["canon_category"])
    question = f"Who won {category} in {row['year_ceremony']}?"

    return render_template("quiz.html",
                           mode=mode,
                           toggle_mode=toggle_mode,
                           toggle_label=toggle_label,
                           question=question,
                           correct_answer=row['name'],
                           category=category,
                           year=row['year_ceremony'],
                           film=row['film'],
                           result=None,
                           show_next=False)

if __name__ == "__main__":
    app.run(debug=True)