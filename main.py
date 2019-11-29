from typing import Dict, Tuple, Sequence
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.utils import np_utils
import pandas as pd
import numpy as np
import json


def load_dataset(path: str) -> str:
    with open(path, "r") as f:
        poems = json.load(f)
        return "\n".join([poem["text"] for poem in poems]).strip().lower()


def create_mapping(text: str) -> (Dict[int, str], Dict[str, int]):
    chars = sorted(list(set(text)))
    return (
        {n: char for n, char in enumerate(chars)},
        {char: n for n, char in enumerate(chars)},
    )


if __name__ == "__main__":
    text = load_dataset("data/poems.json")
    n_to_char, char_to_n = create_mapping(text)
