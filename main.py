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
    text: str, char_to_n: Dict[str, int], chars: [str], seq_length: int
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


def build_model(input_shape: (int, int), output_shape: int) -> Sequential:
    model = Sequential()

    model.add(LSTM(400, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(400))
    model.add(Dropout(0.2))
    model.add(Dense(output_shape, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam")

    return model


def generate(
    starter: str,
    n_to_char: Dict[int, str],
    seq_length: int,
    chars: [str],
    model: Sequential,
) -> str:
    full_string = [n_to_char[value] for value in starter]

    for i in range(seq_length):
        x = np.reshape(starter, (1, len(starter), 1))
        x = x / float(len(chars))

        pred_index = np.argmax(model.predict(x, verbose=0))
        full_string.append(n_to_char[pred_index])

        starter.append(pred_index)
        starter = starter[1 : len(starter)]

    return "".join(full_string)


if __name__ == "__main__":
    seq_length = 100

    text = load_dataset("data/poems.json")

    chars, n_to_char, char_to_n = create_mapping(text)

    X, y = preprocess(text, char_to_n, chars, seq_length)

    model = build_model((X.shape[1], X.shape[2]), y.shape[1])

    model.fit(X, y, epochs=1, batch_size=100)
    model.save_weights("weights/baseline.h5")

    print(generate(X[99], n_to_char, seq_length, chars, model))
