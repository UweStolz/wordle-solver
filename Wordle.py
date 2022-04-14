from typing import List, Set
from random import choice

from CharPos import CharPos
from WordStatus import WordStatus
from words import LANGUAGE, get_word_list


def get_random_word(word_list: Set[str]) -> str:
    random_word = ""
    if len(word_list) > 0:
        random_word = choice(list(word_list))
    return random_word


class Wordle:
    word: str = ""
    word_list: Set[str] = set()
    guesses: List[str] = list()
    correct_chars: Set[CharPos] = set()
    wrong_position_chars: Set[CharPos] = set()
    wrong_chars: Set[str] = set()
    word_status: List[WordStatus] = list()
    word_max_length = 5
    tries: int = 0
    win: bool = False
    language: LANGUAGE

    def __init__(self, tries: int, language: LANGUAGE):
        self.tries = tries
        self.word_list = get_word_list(language)
        self.word = get_random_word(self.word_list)
        self.language = language
        pass

    def reset(self):
        self.word = get_random_word(self.word_list)
        self.guesses = list()
        self.word_status = list()
        self.win = False
        self.correct_chars = set()
        self.wrong_position_chars = set()
        self.wrong_chars = set()
        pass

    def add_guess(self, guess: str):
        guess = guess.upper()

        if len(guess) != self.word_max_length:
            return False

        self.guesses.append(guess)
        return True

    def check_for_game_over(self):
        result = False
        guesses_count = len(self.guesses)
        if guesses_count > 0:
            if guesses_count == self.tries:
                result = True
            if self.word in self.guesses:
                self.win = True
                result = True
        return result

    def check_guess(self, guess: str):
        if self.add_guess(guess):
            status = list()
            for i in range(len(guess)):
                guessed_char = guess[i]
                if guessed_char in self.word:
                    if guessed_char == self.word[i] and guessed_char not in self.correct_chars:
                        status.append(0)
                        charPos = CharPos(i, guessed_char)
                        self.correct_chars.add(charPos)
                    else:
                        status.append(2)
                        charPos = CharPos(i, guessed_char)
                        self.wrong_position_chars.add(charPos)
                else:
                    status.append(1)
                    self.wrong_chars.add(guessed_char)
            self.word_status.append(
                WordStatus(status, guess)
            )
        pass
