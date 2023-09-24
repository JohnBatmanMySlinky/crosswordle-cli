from dataclasses import dataclass
import os

@dataclass
class WordPair:
    word_a: str
    word_b: str
    index_a: int
    index_b: int

def build_dictionary(max_grid_size: int = 10) -> list[WordPair]:
    with open("word_list.txt") as f:
        raw_data = f.readlines()

    dictionary = []
    for line in raw_data:
        a, b = line.strip("\n").split(" ")

        assert len(set(a).intersection(set(b))) > 0
        assert len(a) <= max_grid_size
        assert len(b) <= max_grid_size

        for ia, letter in enumerate(a):
            ib = b.rfind(letter)
            if ib > -1:
                tmp = WordPair(a, b, ia, ib)
                dictionary.append(tmp)
                break

    return dictionary

