from typing import Set
from english_words import english_words_lower_alpha_set
from enum import Enum, unique


@unique
class LANGUAGE(Enum):
    ENGLISH = 1


def filter_word_list(word_list: "set[str]", max_length: int) -> Set[str]:
    filtered_word_list = set()
    for word in word_list:
        if len(word) == max_length:
            filtered_word_list.add(word.upper())

    return filtered_word_list


def get_word_list(language: LANGUAGE, max_length: int = 5):
    if language == LANGUAGE.ENGLISH:
        return filter_word_list(english_words_lower_alpha_set, max_length)
    pass
