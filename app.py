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
    correct = session["correct"]
    wrong = session["wrong"]
    guessed = session["guessed"]
    max_wrong = session["max_wrong"]
    sinister_mode = session.get("sinister", False)

    message = ""
    error = ""

    # Handle Guess
    if request.method == "POST":
        guess = request.form.get("guess", "").lower().strip()

        # Validate guess
        if len(guess) != 1 or guess not in string.ascii_lowercase:
            error = "Please enter a single letter."
        elif guess in guessed:
            error = f"You already guessed '{guess}'."
        else:
            guessed.append(guess)

            if guess in word:
                correct.append(guess)
                message = f"Correct! '{guess}' is in the word."

                # Sinister: change word after correct guess
                if sinister_mode:
                    words = load_words()
                    new_word = sinister_new_word(words, word, correct)
                    word = new_word
                    session["word"] = new_word

            else:
                wrong.append(guess)
                message = f"Incorrect. '{guess}' is not in the word."

    # Build pattern for display
    pattern = get_pattern(word, correct)

    # Win
    if "_" not in pattern:
        return render_template(
            "win.html",
            word=word
        )

    # Lose
    if len(wrong) >= max_wrong:
        return render_template(
            "lose.html",
            word=word,
            ascii=SPACEMAN_PICS[-1]
        )

    # Game Page
    return render_template(
        "game.html",
        pattern=pattern,
        wrong=wrong,
        correct=correct,
        guessed=guessed,
        guesses_left=max_wrong - len(wrong),
        ascii=SPACEMAN_PICS[len(wrong)],
        message=message,
        error=error
    )


@app.route("/reset")
def reset():
    start_new_game()
    return redirect(url_for("game"))


# -------------------------------------------------------
# Run App
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
