from flask import Blueprint, jsonify, render_template

from Solver import Solver
from Wordle import Wordle
from words import LANGUAGE

api = Blueprint("api", __name__, template_folder="templates")

wordle = Wordle(6, LANGUAGE.ENGLISH)
solver = Solver(wordle)


@api.route("/")
def index():
    wordle.reset()
    solver.reset()
    return render_template("index.html")


@api.route("/api/solve")
def solve():
    wordle.reset()
    solver.reset()
    solver.solve_word()

    return jsonify(
        word_solved=wordle.win,
        guesses=wordle.word_status,
        word=wordle.word
    )
