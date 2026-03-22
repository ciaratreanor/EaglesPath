from flask import Flask, render_template, request, redirect, session
from game_logic import QUESTION_DATA, calculate_results

import webbrowser
import socket

def find_free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

app = Flask(__name__)
app.secret_key = "dev-secret"  # required for session storage

@app.route("/")
def index():
    session.clear()
    session["scores"] = [0] * 7
    return render_template("index.html")

@app.route("/quiz/<int:q_index>", methods=["GET", "POST"])
def quiz(q_index):
    if q_index >= len(QUESTION_DATA):
        return redirect("/results")
    
    if request.method == "POST":
        choice = int(request.form["choice"])
        scores = session["scores"]
        for i, val in enumerate(QUESTION_DATA[q_index]["scores"][choice]):
            scores[i] += val
        session["scores"] = scores
        return redirect(f"/quiz/{q_index + 1}")

    if q_index >= len(QUESTION_DATA):
        return redirect("/results")

    return render_template(
        "quiz.html",
        question=QUESTION_DATA[q_index],
        q_index=q_index
    )

@app.route("/results")
def results():
    results = calculate_results(session["scores"])
    return render_template("results.html", results=results)

if __name__ == "__main__":
    port = find_free_port()
    webbrowser.open(f"http://127.0.0.1:{port}")
    app.run(debug=False, port=port)
