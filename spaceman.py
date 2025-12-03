from flask import Flask, render_template, request, session, redirect, url_for
import random
import string
from pathlib import Path

app = Flask(__name__)
app.secret_key = "super-secret-change-this"


# =============================
# ASCII ART FOR SPACEMAN
# =============================
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


# =============================
# LOAD WORDS
# =============================
def load_words():
    if Path("words.txt").exists():
        with open("words.txt", "r") as f:
            return f.read().split()
    return ["car", "cat", "bar", "bat", "star", "space", "python", "rocket"]


# =============================
# SINISTER MODE HELPERS
# =============================
def get_pattern(word, guessed_correct):
    return "".join([letter if letter in guessed_correct else "_" for letter in word])


def word_matches_pattern(candidate, pattern, guessed_correct):
    for c1, c2 in zip(candidate, pattern):
        if c2 != "_" and c1 != c2:
            return False
        if c1 in guessed_correct and c2 == "_":
            return False
    return True


def pick_new_sinister_word(words, current_word, guessed_correct):
    pattern = get_pattern(current_word, guessed_correct)
    candidates = [
        w for w in words
        if len(w) == len(current_word) and word_matches_pattern(w, pattern, guessed_correct)
    ]
    return random.choice(candidates) if candidates else current_word


# =============================
# NEW GAME INITIALIZATION
# =============================
def start_new_game():
    words = load_words()
    word = random.choice(words)

    session["word"] = word
    session["words"] = words
    session["guessed_correct"] = []
    session["guessed_wrong"] = []
    session["guessed_all"] = []
    session["max_wrong"] = len(word)
    session["game_over"] = False
    session["won"] = False


# =============================
# ROUTES
# =============================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    start_new_game()
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    # Prevent playing without starting
    if "word" not in session:
        return redirect(url_for("start"))

    word = session["word"]
    guessed_correct = set(session["guessed_correct"])
    guessed_wrong = set(session["guessed_wrong"])
    guessed_all = set(session["guessed_all"])
    max_wrong = session["max_wrong"]
    words = session["words"]

    message = None

    if request.method == "POST" and not session.get("game_over"):
        guess = request.form.get("guess", "").lower().strip()

        # Validation
        if len(guess) != 1 or guess not in string.ascii_lowercase:
            message = "❗ Please enter a single valid letter."
        elif guess in guessed_all:
            message = "⚠ You already guessed that!"
        else:
            guessed_all.add(guess)
            session["guessed_all"] = list(guessed_all)

            if guess in word:
                guessed_correct.add(guess)
                session["guessed_correct"] = list(guessed_correct)

                # SINISTER MODE
                new_word = pick_new_sinister_word(words, word, guessed_correct)
                session["word"] = new_word
                word = new_word
                message = f"✅ Correct! '{guess}' is in the word."
            else:
                guessed_wrong.add(guess)
                session["guessed_wrong"] = list(guessed_wrong)
                message = f"❌ '{guess}' is NOT in the word."

    pattern = get_pattern(word, guessed_correct)

    # Win condition
    if "_" not in pattern:
        session["game_over"] = True
        session["won"] = True

    # Loss condition
    if len(guessed_wrong) >= max_wrong:
        session["game_over"] = True
        session["won"] = False

    # Choose ASCII art
    ascii_art = SPACEMAN_PICS[min(len(guessed_wrong), len(SPACEMAN_PICS) - 1)]

    return render_template(
        "game.html",
        pattern=pattern,
        wrong_guesses=guessed_wrong,
        guessed_all=guessed_all,
        max_wrong=max_wrong,
        ascii_art=ascii_art,
        message=message,
        game_over=session["game_over"],
        won=session["won"],
        word=word  # reveal on loss
    )


@app.route("/restart")
def restart():
    start_new_game()
    return redirect(url_for("game"))


if __name__ == "__main__":
    app.run(debug=True)
