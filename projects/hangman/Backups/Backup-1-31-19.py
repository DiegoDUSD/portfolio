from __future__ import print_function
import random

def hangman_display(guessed, secret):
    """Returns a secret with dashes for letters which have not been guessed.
    Arguments:

    guessed - a string which contains all the characters which are guessed by
    the user.

    secret - the string which is guessed at by the user."""
    result = ""
    # Go through all the characters needed to be printed
    for char in secret:
        # Condition for if the letter has been guessed or whitespace
        if char.lower() in guessed.lower() or char == " ":
            result += char
            continue
        # Print unguessed character
        result += "-"
    return result

def is_done_guessing(guessed, secret):
    """This determines if a word has been guessed from the inputted characters.

    guessed - the characters which have been guessed by the player.

    secret - the word which is attempted to be guessed."""
    return hangman_display(guessed, secret) == secret


def hangman():
    """This returns nothing and begins the hangman game. It will ask the user to
    make a guess for the word. This game gives the user 7 chances to win the
    game. This takes no arguments and returns nothing."""

    word_list = ["Alexander the Great", "Napoleon", "Philip of Macedon",
    "Henry of England", "Judas Iscariot", "The Enlightenment",
    "Leonardo da Vinci", "Adolf Hitler", "Winston Churchill",
    "Teddy Roosevelt", "Martin van Buren", "Abraham Lincoln",
    "George Washington", "Peter the Great", "Pope Francis",
    "Ludwig van Beethoven", "Maximillien Robespierre", "Leopold of Belgium",
    "Augustus Caesar", "Plato", "Maximilian Holy Roman Emperor", "Louis XVI",
    "Otto von Bismarck", "Emperor Hirohito", "Emperor Meiji", "Erwin Rommel",
    "Robert E Lee", "Catherine the Great", "Queen Victoria", "Chandragupta",
    "Joseph Stalin", "Benito Mussolini", "Charlemagne", "Charles the Bold",
    "Dirk Fock", "Pieter Mijer", "Alexander Graham Bell", "Neil Armstrong",
    "Woodrow Wilson", "Mao Zedong", "Cleopatra", "Ho Chi Minh",
    "William Shakespeare"]

    guess_count = 7

    # Print the header
    print("Hangman Game - Seven Chances")
    print("Type \"Hint\" to get a hint.")

    # Set up the secret
    secret = random.choice(word_list)
    guessed_letters = ""
    if print_secret:
        print("DEV MODE: The secret is \"", secret, "\"", sep="")

    # Print the format of the string being guessed
    print(hangman_display(guessed_letters, secret))
    while not is_done_guessing(guessed_letters, secret) and guess_count > 0:
        # Get the guess
        guess = raw_input("\nMake a guess for a letter: ").lower()
        # Checks that the input is only one letter
        if guess.lower() == "hint":
            # This will reveal one character which has not been guessed
            for secret_char in secret:
                # This means that the character has already been guessed by the
                # user
                if secret_char in guessed_letters:
                    continue
                # This is under the condition that this secret_char has not been
                # guessed by the user yet, which means it can be used as a hint
                secret_char = secret_char.lower()
                guessed_letters += secret_char
                print("Your hint is: One of the characters is", secret_char)
                break
            print(hangman_display(guessed_letters, secret))
            continue
        
        if guess == secret.lower():
            print("You guessed the word!")
            guessed_letters += secret.lower()
            break
        
        if len(guess) == 0:
            print("You didn't guess one letter!")
            continue
        
        if len(guess) != 1:
            print("You failed to guess the whole word.")
            guess_count -= 1
            print("You have", guess_count, "guesses left.")
            # Skips the current loop and goes back to the while condition
            continue
        # If the letter has already been guessed, this will print an error
        # statement.
        if guess in guessed_letters:
            print("You already guessed this.")
            continue
        guessed_letters += guess

        # Determines if the guess is correct
        if guess.lower() not in secret.lower():
            guess_count -= 1
            print("You guessed incorrectly.")
            print("You have", guess_count, "guesses left.")

        print(hangman_display(guessed_letters, secret))
    if is_done_guessing(guessed_letters, secret):
        # Condition upon which the user has guessed remaining when the game ends
        # This is a win
        print("\nCongratulations! You won!")
    else:
        # This is a lose
        print("\nYou lost!")
        print("The word was:", secret)
    replay_in = raw_input("Replay? (y/n) ")
    if replay_in.lower() == "y":
        hangman()

# Dev mode
print_secret = True