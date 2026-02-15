import csv
import random
from collections import defaultdict

CSV_FILE = "the_oscar_award.csv"


# ---------------------------
# Data Loading
# ---------------------------

def load_data(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_winners(data):
    return [row for row in data if row["winner"].lower() == "true"]


def group_by_year_category(winners):
    grouped = defaultdict(list)
    for row in winners:
        key = (row["year_ceremony"], row["canon_category"])
        grouped[key].append(row)
    return grouped


# ---------------------------
# Question Types
# ---------------------------

def q_winner_by_year(grouped):
    (year, category), winners = random.choice(list(grouped.items()))
    names = list(set(w["name"] for w in winners))
    return {
        "question": f"Who won {category} in {year}?",
        "correct_answer": ", ".join(names),
        "choices": None
    }


def q_film_to_award(winners):
    row = random.choice(winners)
    if not row["film"]:
        return q_film_to_award(winners)

    return {
        "question": f"What award did '{row['film']}' win in {row['year_ceremony']}?",
        "correct_answer": row["canon_category"],
        "choices": None
    }


def q_person_to_award(winners):
    row = random.choice(winners)
    return {
        "question": f"What award did {row['name']} win in {row['year_ceremony']}?",
        "correct_answer": row["canon_category"],
        "choices": None
    }


def q_guess_year(winners):
    row = random.choice(winners)
    return {
        "question": f"In what year did {row['name']} win {row['canon_category']}?",
        "correct_answer": row["year_ceremony"],
        "choices": None
    }


def q_true_false(data):
    row = random.choice(data)
    statement = f"{row['name']} won {row['canon_category']} in {row['year_ceremony']}."

    correct = "True" if row["winner"].lower() == "true" else "False"

    return {
        "question": f"True or False: {statement}",
        "correct_answer": correct,
        "choices": ["True", "False"]
    }


def q_multiple_choice(grouped, winners):
    (year, category), correct_rows = random.choice(list(grouped.items()))
    correct_name = correct_rows[0]["name"]

    wrong_options = [
        w["name"] for w in winners
        if w["name"] != correct_name
    ]

    choices = random.sample(wrong_options, min(3, len(wrong_options)))
    choices.append(correct_name)
    random.shuffle(choices)

    return {
        "question": f"Who won {category} in {year}?",
        "correct_answer": correct_name,
        "choices": choices
    }


# ---------------------------
# Quiz Engine
# ---------------------------

def generate_random_question(data, winners, grouped):
    question_types = [
        lambda: q_winner_by_year(grouped),
        lambda: q_film_to_award(winners),
        lambda: q_person_to_award(winners),
        lambda: q_guess_year(winners),
        lambda: q_true_false(data),
        lambda: q_multiple_choice(grouped, winners),
    ]

    return random.choice(question_types)()


def ask_question(q):
    print("\n" + q["question"])

    if q["choices"]:
        for i, choice in enumerate(q["choices"], 1):
            print(f"{i}. {choice}")

        user_input = input("Your answer (number): ")

        if user_input.isdigit():
            selected = q["choices"][int(user_input) - 1]
        else:
            selected = user_input
    else:
        selected = input("Your answer: ")

    if selected.strip().lower() in q["correct_answer"].lower():
        print("✅ Correct!")
        return True
    else:
        print(f"❌ Incorrect. Correct answer: {q['correct_answer']}")
        return False


def run_quiz():
    data = load_data(CSV_FILE)
    winners = get_winners(data)
    grouped = group_by_year_category(winners)

    score = 0
    rounds = 10

    print("🏆 Academy Awards Ultimate Quiz 🏆")

    for i in range(rounds):
        q = generate_random_question(data, winners, grouped)
        if ask_question(q):
            score += 1

    print(f"\nFinal Score: {score}/{rounds}")


if __name__ == "__main__":
    run_quiz()

