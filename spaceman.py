import random

def load_word():
    '''
    A function that reads a text file of words and randomly selects one to use as the secret word
        from the list.
    '''
    f = open('words.txt', 'r')
    words_list = f.readlines()
    f.close()
    
    words_list = words_list[0].split(' ') 
    secret_word = random.choice(words_list)
    return secret_word.strip().lower()



def is_word_guessed(secret_word, letters_guessed):
    '''
    Returns True only if all the letters of secret_word are in letters_guessed.
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    Returns the current guessed word with letters and underscores.
    Example: secret = "apple", guessed = ['p']
             returns "_ pp_ _"
    '''
    result = ""
    for letter in secret_word:
        if letter in letters_guessed:
            result += letter
        else:
            result += "_"
    return result



def is_guess_in_word(guess, secret_word):
    '''
    Returns True if guess is in the secret word, otherwise False.
    '''
    return guess in secret_word



def spaceman(secret_word):
    '''
    Runs the main game loop for Spaceman.
    '''

    print("🛸 Welcome to Spaceman!")
    print(f"The secret word has {len(secret_word)} letters.")
    print("You have 7 incorrect guesses. Good luck!\n")

    letters_guessed = []
    incorrect_guesses = 0
    max_incorrect = 7

    # Game loop
    while incorrect_guesses < max_incorrect:

        print("Current word:", get_guessed_word(secret_word, letters_guessed))
        print(f"Incorrect guesses left: {max_incorrect - incorrect_guesses}")

        # Ask for guess
        guess = input("Guess a letter: ").lower().strip()

        # Enforce single-letter input
        if len(guess) != 1 or not guess.isalpha():
            print("❗ Please guess exactly ONE letter.\n")
            continue

        # Alert if repeated guess
        if guess in letters_guessed:
            print("⚠ You already guessed that letter!\n")
            continue

        letters_guessed.append(guess)

        # Check guess correctness
        if is_guess_in_word(guess, secret_word):
            print("✅ Correct guess!\n")
        else:
            print("❌ Incorrect guess.\n")
            incorrect_guesses += 1

        # Check win state
        if is_word_guessed(secret_word, letters_guessed):
            print("🎉 YOU WIN! The word was:", secret_word)
            return

    # Loss condition
    print("💀 You've run out of guesses! You lost.")
    print("The secret word was:", secret_word)


