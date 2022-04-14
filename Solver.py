from typing import Set
from collections import Counter
from random import choice

from logger import logger
from CharPos import CharPos
from Wordle import Wordle


def get_random_word_with_unique_chars(word_list):
    word = None
    size = len(word_list)
    if size > 0:
        for _i in range(size):
            word = choice(list(word_list))
            freq = Counter(word)
            if(len(freq) == len(word)):
                break
    return word


def get_word(word_list: Set[str]) -> str:
    word = get_random_word_with_unique_chars(word_list)
    if not word:
        word = word_list.pop()
    return word


class Solver:
    wordle: Wordle
    guess: str = ""
    possible_words: Set[str] = set()
    correct_chars: Set[CharPos] = set()
    wrong_position_chars: Set[CharPos] = set()
    wrong_chars: Set[str] = set()

    def __init__(self, wordle: Wordle) -> None:
        self.wordle = wordle
        pass

    def reset(self):
        self.possible_words = set()
        self.correct_chars = set()
        self.wrong_position_chars = set()
        self.wrong_chars_index = set()
        self.guess = ""
        pass

    def filter_words_with_char_not_at_position(self):
        correct_chars = self.wordle.correct_chars - self.correct_chars
        if (len(correct_chars)) > 0:
            logger.info("Correct char count: {}", len(correct_chars))
            words = self.possible_words.copy()
            for charPos in correct_chars:
                logger.info("\tCorrect char: {}  {}",
                            charPos.char, charPos.position+1)
                for word in words:
                    if not word[charPos.position] == charPos.char:
                        self.possible_words.discard(word)
            self.correct_chars = self.wordle.correct_chars.copy()
        pass

    def filter_words_with_char_at_position(self):
        wrong_position_chars = self.wordle.wrong_position_chars - self.wrong_position_chars
        if (len(wrong_position_chars)) > 0:
            logger.info("Wrong position char count: {}",
                        len(wrong_position_chars))
            words = self.possible_words.copy()
            for charPos in wrong_position_chars:
                logger.info("\tCorrect char, wrong position: {}",
                            charPos.char, charPos.position+1)
                for word in words:
                    if charPos.char not in word or charPos.char == word[charPos.position]:
                        self.possible_words.discard(word)
            self.wrong_position_chars = self.wordle.wrong_position_chars.copy()
        pass

    def filter_wrong_words(self):
        wrong_chars = self.wordle.wrong_chars - self.wrong_chars
        if (len(wrong_chars)) > 0:
            logger.info("Wrong char count: {}", len(wrong_chars))
            words = self.possible_words.copy()
            for char in wrong_chars:
                logger.info("\tWrong char: {}", char)
                for word in words:
                    if char in word:
                        self.possible_words.discard(word)
            self.wrong_chars = self.wordle.wrong_chars.copy()
        pass

    def filter_words(self):
        # Correct char, correct position
        self.filter_words_with_char_not_at_position(),

        # Correct char, wrong position
        self.filter_words_with_char_at_position()

        # Wrong char in word
        self.filter_wrong_words()
        pass

    def solve_word(self):
        # First run
        logger.info("Word: {}", self.wordle.word)
        logger.info("Word list: {}", len(self.wordle.word_list))
        self.possible_words = self.wordle.word_list.copy()
        self.guess = get_word(self.possible_words)
        logger.info("Guess-1: {}", self.guess)
        self.wordle.check_guess(self.guess)

        # Subsequent runs, if not directly solved
        if not self.wordle.check_for_game_over():
            self.possible_words -= {self.guess}
            logger.info("Possible words: {}", len(self.possible_words))
            self.filter_words()
            logger.info("Possible words: {}", len(self.possible_words))
            logger.info("-----------------------------------------")

            for index in range(1, self.wordle.tries):
                possible_word_count = len(self.possible_words)
                if possible_word_count > 1:
                    self.guess = get_word(self.possible_words)
                    self.possible_words -= {self.guess}
                    logger.info("Guess-{}: {}", index+1, self.guess)
                    self.wordle.check_guess(self.guess)
                    if self.wordle.check_for_game_over():
                        break
                    else:
                        self.filter_words()
                elif possible_word_count == 1:
                    self.guess = self.possible_words.pop()
                    logger.info("1 possible word left")
                    logger.info("Guess-{}: {}", index+1, self.guess)
                    self.wordle.check_guess(self.guess)
                    self.wordle.check_for_game_over()
                    break
                else:
                    logger.info("No possible words")
                    break
                logger.info("Possible words: {}", len(self.possible_words))
                logger.info("-----------------------------------------")
                pass
            logger.info("Possible answers left: {}", len(self.possible_words))
        if self.wordle.win:
            logger.info("Correct Guess: {}\n", self.guess)
        else:
            logger.info("No correct guess\n")
        self.reset()
        pass
