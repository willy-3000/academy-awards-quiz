import os
import csv
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Load Oscar winners CSV into a list of dictionaries
def load_winners():
    winners = []
    with open("oscars.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            winners.append(row)
    return winners

winners_data = load_winners()

# Define easy categories
EASY_CATEGORIES = ["ACTOR IN A LEADING ROLE", "ACTRESS IN A LEADING ROLE", "BEST PICTURE", "DIRECTOR"]

@app.route("/", methods=["GET", "POST"])
def quiz():
    mode = request.values.get("mode", "easy")
    show_next = False
    show_skip = True
    result = None

    if mode == "easy":
        data = [w for w in winners_data if w["canon_category"] in EASY_CATEGORIES]
    else:
        data = winners_data

    if request.method == "POST":
            user_answer = request.form.get("answer", "").strip().lower()
            correct_answer = request.form.get("correct_answer", "").strip().lower()
            category = request.form.get("category")
            year = request.form.get("year")
            film = request.form.get("film", "")

            if user_answer == correct_answer:
                result = f"Correct! {correct_answer.title()} won in {year} for {film}."
            else:
                result = f"Wrong! The correct answer was {correct_answer.title()} for {film}."
            
            show_skip = False
            show_next = True

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = request.form.get("correct_answer", "").strip().lower()
        category = request.form.get("category")
        year = request.form.get("year")
        film = request.form.get("film")

    if user_answer == correct_answer:
        result = f"Correct! {correct_answer.title()} won in {year} for {film}."
    else:
        result = f"Wrong! The correct answer was {correct_answer.title()} for {film}."

    show_skip = False
    show_next = True

    # KEEP SAME QUESTION
    question = f"Who won {category} in {year}?"

    else:
        question_item = random.choice(data)
        question = f"Who won {question_item['canon_category']} in {question_item['year_ceremony']}?"
        correct_answer = question_item["name"]
        category = question_item["canon_category"]
        year = question_item["year_ceremony"]
        film = question_item["film"]

        toggle_mode = "hard" if mode == "easy" else "easy"
        toggle_label = "Switch to Hard Mode" if mode == "easy" else "Switch to Easy Mode"

    return render_template(
        "quiz.html",
        question=question,
        correct_answer=correct_answer,
        category=category,
        year=year,
        film=film,
        result=result,
        show_next=show_next,
        show_skip=show_skip,
        mode=mode,
        toggle_mode=toggle_mode,
        toggle_label=toggle_label
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)