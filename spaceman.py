import random
import string

# =============================
# ASCII ART FOR THE SPACEMAN
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

# Load words from file
def load_words(filename="words.txt"):
    try:
        with open(filename, "r") as f:
            words_list = f.read().split()
            return words_list
    except FileNotFoundError:
        # fallback list
        return ["cat", "bar", "bat", "car", "star", "space", "python", "rocket"]

# =============================
# SINISTER WORD CHANGER
# =============================

def pick_new_sinister_word(words, current_word, guessed_correct):
    """Pick a new word with:
       - same length
       - fits all correctly guessed letters in the same positions
    """
    pattern = get_pattern(current_word, guessed_correct)

    valid_candidates = []
    for w in words:
        if len(w) != len(current_word):
            continue
        if word_matches_pattern(w, pattern, guessed_correct):
            valid_candidates.append(w)

    if valid_candidates:
        return random.choice(valid_candidates)
    return current_word  # fallback (should rarely happen)


def get_pattern(word, guessed_correct):
    """Return pattern like a_b_ for a word & guessed letters."""
    return "".join([letter if letter in guessed_correct else "_" for letter in word])


def word_matches_pattern(candidate, pattern, guessed_correct):
    """Check if candidate fits the pattern and does not break previously matched letters."""
    for c1, c2 in zip(candidate, pattern):
        if c2 != "_" and c1 != c2:
            return False
        # cannot contradict a known correct letter
        if c1 in guessed_correct and c2 == "_":
            return False
    return True

# =============================
# MAIN GAME LOGIC
# =============================

def display_game_state(pattern, guessed_wrong, max_guesses):
    print("\nCurrent Word: ", " ".join(pattern))
    print(f"Wrong guesses ({len(guessed_wrong)}/{max_guesses}): {', '.join(guessed_wrong)}")
    print(SPACEMAN_PICS[len(guessed_wrong)])
    print("-" * 30)


def get_valid_letter(guessed_all):
    while True:
        guess = input("Guess a letter → ").lower().strip()
        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print("❗ Please enter **one single letter**.")
            continue
        if guess in guessed_all:
            print("⚠ You already guessed that letter! Try another.")
            continue
        return guess


def play_spaceman():
    print("\n🛸 Welcome to SINISTER SPACEMAN! 🛸")

    words = load_words()
    chosen_word = random.choice(words)
    word_length = len(chosen_word)
    max_wrong_guesses = word_length

    guessed_correct = set()
    guessed_wrong = set()
    guessed_all = set()

    print(f"\nThe mystery word has {word_length} letters.")

    while True:
        pattern = get_pattern(chosen_word, guessed_correct)
        display_game_state(pattern, guessed_wrong, max_wrong_guesses)

        # Win condition
        if "_" not in pattern:
            print("🎉 YOU WIN! The word was:", chosen_word)
            break

        # Loss condition
        if len(guessed_wrong) >= max_wrong_guesses:
            print("💀 You lost!")
            print("The mystery word was:", chosen_word)
            break

        guess = get_valid_letter(guessed_all)
        guessed_all.add(guess)

        # Correct guess
        if guess in chosen_word:
            print(f"✅ Correct! '{guess}' is in the word.")
            guessed_correct.add(guess)

            # --- SINISTER MODE ---
            # After showing them the correct letter, we change the word!
            new_word = pick_new_sinister_word(words, chosen_word, guessed_correct)
            chosen_word = new_word

        else:
            print(f"❌ Incorrect. '{guess}' is NOT in the word.")
            guessed_wrong.add(guess)


# =============================
# PLAY AGAIN LOOP
# =============================

def main():
    while True:
        play_spaceman()
        again = input("\nPlay again? (y/n) → ").lower().strip()
        if again != "y":
            print("\n🚀 Thanks for playing Spaceman!")
            break


if __name__ == "__main__":
    main()