###############################################################################
# FILE : hangman.py
# WRITER : Seggev Haimovich , seggev , 206729295
# EXERCISE : intro2cs2 ex4 2021
# DESCRIPTION: The game hangman
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: none
###############################################################################

import hangman_helper


def start_game(words_list, score):
    """
    sets the initial variables for the game and prints the start of the game.
    :param words_list: list
    :param score: int
    :return: word (string), wrong guess list (list), pattern (string)
    """
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_list = []
    pattern = '_' * len(word)
    hangman_helper.display_state(pattern, wrong_guess_list, score, 'WELCOME '
                                                                   'TO THE '
                                                                   'BEST GAME '
                                                                   'EVER')
    return word, wrong_guess_list, pattern


def update_word_pattern(word, pattern, letter):
    """
    gets the goal word, the current pattern and the guess of the user.
    returns the new pattern after updating it.
    :param word: string
    :param pattern: string
    :param letter: string
    :return: string
    """
    new_pattern_list = [word[i] if word[i] == letter else pattern[i] for i
                        in range(len(word))]
    new_pattern = ''.join(new_pattern_list)
    return new_pattern


def filter_words_list(words, pattern, wrong_guess_list):
    """
    gets the words bank, the current pattern and the list of the wrong
    guesses the user already guessed.
    returns the list of the words in the bank that matches the current pattern.
    :param words: list
    :param pattern: string
    :param wrong_guess_list: list
    :return: list
    """
    hint_list = []
    for word in words:
        if len(word) != len(pattern):  # reject the words with the wrong length
            continue
        are_they_equal = True
        for letter in range(len(pattern)):
            if word[letter] in wrong_guess_list:
                are_they_equal = False
                break
            if pattern[letter] != '_':
                if pattern[letter] != word[letter]:
                    are_they_equal = False
                    break
                if pattern.count(pattern[letter]) != word.count(word[letter]):
                    # checks if the pattern and the word have the same
                    # amount of the same letters, if not they are not equal
                    are_they_equal = False
                    break
        if are_they_equal:
            hint_list.append(word)
    return hint_list


def problem_guess(wrong_guess_list, pattern, guess, score):
    """
    checks if the guess is problematic
    :param wrong_guess_list: list
    :param pattern: string
    :param guess: string
    :param score: int
    :return: bool (True if there is a problem, False otherwise)
    """
    if len(guess) != 1:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                     'You entered an invalid letter')
        return True
    if not guess.islower():  # checks if the letter is lower case
        hangman_helper.display_state(pattern, wrong_guess_list,
                                     score, 'You entered an invalid '
                                            'letter')
        return True
    if guess in pattern or guess in wrong_guess_list:
        hangman_helper.display_state(pattern, wrong_guess_list,
                                     score, 'You have already '
                                            'guessed this letter')
        return True
    return False


def play_letter(word, wrong_guess_list, pattern, guess, score):
    """
    play 1 step of the game after the player guessed a letter
    :param word: string
    :param wrong_guess_list: list
    :param pattern: string
    :param guess: string
    :param score: int
    :return: pattern (string), score (int)
    """
    score -= 1
    if guess not in word:
        wrong_guess_list.append(guess)
    n = word.count(guess)
    score += n * (n + 1) // 2
    pattern = update_word_pattern(word, pattern, guess)
    return pattern, score


def play_word(word, pattern, guess, score):
    """
    play 1 step of the game after the player guessed a word
    :param word: string
    :param pattern: string
    :param guess: string
    :param score: int
    :return: pattern (string), score (int)
    """
    score -= 1
    if guess == word:
        n = pattern.count('_')
        score += n * (n + 1) // 2
        pattern = word
    return pattern, score


def play_hint(score, words_list, pattern, wrong_guess_list):
    """
    play 1 step of the game after the player asked for a hint
    :param score: int
    :param words_list: list
    :param pattern: string
    :param wrong_guess_list: list
    :return: score (int)
    """
    score -= 1
    hint_list = filter_words_list(words_list, pattern, wrong_guess_list)
    new_hint_list = hint_list
    if len(hint_list) > hangman_helper.HINT_LENGTH:
        new_hint_list = []
        for i in range(hangman_helper.HINT_LENGTH):
            new_hint_list.append(hint_list[i * len(
                hint_list) // hangman_helper.HINT_LENGTH])
    hangman_helper.show_suggestions(new_hint_list)
    return score


def end_game(pattern, word, wrong_guess_list, score):
    """
    checks if the game should be ended and prints the end massage
    :param pattern: string
    :param word: string
    :param wrong_guess_list: list
    :param score: int
    :return: bool (True if the game should be ended, False otherwise)
    """
    if pattern == word:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                     'YOU WON THE GAME')
        return True
    elif score == 0:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                     'You lost the game, the word was: ' +
                                     word)
        return True
    return False


def run_single_game(words_list, score):
    """
    gets the words bank and the initial score.
    runs 1 game of hangman and return the final score of the user.
    :param words_list: list
    :param score: int
    :return: int
    """
    word, wrong_guess_list, pattern = start_game(words_list, score)
    while score > 0:
        guess_type, guess = hangman_helper.get_input()
        if guess_type == hangman_helper.LETTER:
            if problem_guess(wrong_guess_list, pattern, guess, score):
                continue
            pattern, score = play_letter(word, wrong_guess_list, pattern,
                                         guess, score)
        elif guess_type == hangman_helper.WORD:
            pattern, score = play_word(word, pattern, guess, score)
        else:
            score = play_hint(score, words_list, pattern, wrong_guess_list)
        if end_game(pattern, word, wrong_guess_list, score):
            break
        hangman_helper.display_state(pattern, wrong_guess_list, score, '')
    return score


def main():
    """
    runs the game hangman as many times as the user wants.
    if the user wins a game, it give him the opportunity to play one more
    time and to collect the points he has.
    if the user loses it gives him the chance to try one more time with the
    initial points.
    :return: None
    """
    words_list = hangman_helper.load_words()
    points = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
    number_of_games = 1
    while True:
        if points == 0 and hangman_helper.play_again(f"You survived "
                                                     f"{number_of_games} "
                                                     f"games.\nWould you "
                                                     f"like to start a new"
                                                     f" series of games?"):
            number_of_games = 1
            points = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
            continue
        if points != 0 and hangman_helper.play_again(f"So far you played "
                                                     f"{number_of_games} games"
                                                     f" and you have earned "
                                                     f"{points} points.\nWould"
                                                     f" you like to play "
                                                     f"another one?"):
            number_of_games += 1
            points = run_single_game(words_list, points)
            continue
        break


if __name__ == "__main__":
    main()
