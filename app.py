from flask import Flask, render_template, request, redirect, session, url_for
import random
import string

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_CHANGE_THIS"  # Required for session cookies


# -------------------------------------------------------
# ASCII Art (optional, you can display or not)
# -------------------------------------------------------
SPACEMAN_PICS = [
    """
       +---+
           |
           |
           |
          ===""",
    """
       +---+
       O   |
           |
           |
          ===""",
    """
       +---+
       O   |
       |   |
           |
          ===""",
    """
       +---+
       O   |
      /|   |
           |
          ===""",
    """
       +---+
       O   |
      /|\\  |
           |
          ===""",
    """
       +---+
       O   |
      /|\\  |
      /    |
          ===""",
    """
       +---+
       O   |
      /|\\  |
      / \\  |
          ==="""
]


# -------------------------------------------------------
# Load word list
# -------------------------------------------------------
def load_words(filename="words.txt"):
    try:
        with open(filename, "r") as f:
            return f.read().split()
    except FileNotFoundError:
        return ["cat", "bar", "bat", "car", "star", "space",
                "python", "rocket", "planet", "galaxy"]


# -------------------------------------------------------
# Game Helper Functions
# -------------------------------------------------------
def get_pattern(word, correct_letters):
    """Pattern like _ a _ _ e"""
    return "".join([c if c in correct_letters else "_" for c in word])


def word_matches_pattern(candidate, pattern, correct_letters):
    """Ensure candidate fits pattern & doesn't break known letters"""
    for c1, c2 in zip(candidate, pattern):
        if c2 != "_" and c1 != c2:
            return False
        if c1 in correct_letters and c2 == "_":
            return False
    return True


def sinister_new_word(words, current_word, correct_letters):
    """Sinister mode: word changes but keeps same length & revealed letters"""
    pattern = get_pattern(current_word, correct_letters)
    candidates = [
        w for w in words
        if len(w) == len(current_word)
        and word_matches_pattern(w, pattern, correct_letters)
    ]
    return random.choice(candidates) if candidates else current_word


# -------------------------------------------------------
# Start a new game (never redirects - prevents loops)
# -------------------------------------------------------
def start_new_game():
    words = load_words()
    word = random.choice(words)
    session["word"] = word
    session["correct"] = []
    session["wrong"] = []
    session["guessed"] = []
    session["max_wrong"] = len(word)
    session["sinister"] = True  # Toggle sinister mode ON/OFF


# -------------------------------------------------------
# Routes
# -------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    start_new_game()
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():

    # SAFETY: Instead of redirecting → just start a new game
    if "word" not in session:
        start_new_game()

    word = session["word"]
    correct = session["correct"]()
