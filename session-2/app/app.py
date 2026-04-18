from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

OPTIONS = [
    "Never used it",
    "Heard of it, but never used it",
    "Used it a little",
    "Fairly comfortable with it",
]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///poll.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, future=True)


def init_db() -> None:
    if DATABASE_URL.startswith("postgresql://"):
        create_sql = """
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL PRIMARY KEY,
            option_name TEXT NOT NULL
        )
        """
    else:
        create_sql = """
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            option_name TEXT NOT NULL
        )
        """

    with engine.begin() as conn:
        conn.execute(text(create_sql))


@app.route("/", methods=["GET"])
def index():
    return render_template("poll.html", options=OPTIONS)


@app.route("/vote", methods=["POST"])
def vote():
    selected = request.form.get("option")

    if selected not in OPTIONS:
        return "Invalid option", 400

    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO votes (option_name) VALUES (:option_name)"),
            {"option_name": selected},
        )

    return redirect(url_for("results"))


@app.route("/results", methods=["GET"])
def results():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM votes")).scalar_one()

        rows = conn.execute(
            text(
                """
                SELECT option_name, COUNT(*) AS count
                FROM votes
                GROUP BY option_name
                """
            )
        ).all()

    counts = {option: 0 for option in OPTIONS}
    for option_name, count in rows:
        counts[option_name] = count

    results_data = []
    for option in OPTIONS:
        count = counts[option]
        percentage = (count / total * 100) if total > 0 else 0
        results_data.append(
            {
                "option": option,
                "count": count,
                "percentage": round(percentage, 1),
            }
        )

    return render_template(
        "results.html",
        question="How much experience do you have with Docker?",
        total=total,
        results=results_data,
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)
else:
    init_db()

