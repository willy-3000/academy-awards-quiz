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
        # Get submitted data
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = request.form.get("correct_answer", "").strip().lower()
        category = request.form.get("category")
        year = request.form.get("year")
        film = request.form.get("film", "")

        # Check answer
        if user_answer == correct_answer:
            result = f"Correct! {correct_answer.title()} won in {year} for {film}."
        else:
            result = f"Wrong! The correct answer was {correct_answer.title()} for {film}."

        show_skip = False
        show_next = True

        # KEEP SAME QUESTION
        question = f"Who won {category} in {year}?"

    else:
        # Generate new question only on GET
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
