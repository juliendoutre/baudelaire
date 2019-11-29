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


def create_mapping(text: str) -> ([str], Dict[int, str], Dict[str, int]):
    chars = sorted(list(set(text)))
    return (
        chars,
        {n: char for (n, char) in enumerate(chars)},
        {char: n for (n, char) in enumerate(chars)},
    )


def preprocess(
    text: str, char_to_n: Dict[str, int], chars: [str], seq_length: int = 100
) -> (np.matrix, np.matrix):
    X, Y = [], []
    length = len(text)

    for i in range(length - seq_length):
        sequence = text[i : i + seq_length]
        label = text[i + seq_length]

        X.append([char_to_n[char] for char in sequence])
        Y.append(char_to_n[label])

        return (
            np.reshape(X, (len(X), seq_length, 1)) / float(len(chars)),
            np_utils.to_categorical(Y),
        )


if __name__ == "__main__":
    text = load_dataset("data/poems.json")

    chars, n_to_char, char_to_n = create_mapping(text)

    X, y = preprocess(text, char_to_n, chars)
