#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.utils import np_utils
from typing import Dict
import numpy as np
import random
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
) -> (np.matrix, np.matrix, np.matrix):
    X, Y = [], []
    length = len(text)

    for i in range(length - seq_length):
        sequence = text[i : i + seq_length]
        label = text[i + seq_length]

        X.append([char_to_n[char] for char in sequence])
        Y.append(char_to_n[label])

    return (
        X,
        np.reshape(X, (len(X), seq_length, 1)) / float(len(chars)),
        np_utils.to_categorical(Y),
    )


def build_model(input_shape: (int, int), output_shape: int) -> Sequential:
    model = Sequential()

    model.add(LSTM(700, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(700, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(700))
    model.add(Dropout(0.2))
    model.add(Dense(output_shape, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam")

    return model


def generate(
    starter: np.array, seq_length: int, chars: [str], model: Sequential,
) -> np.array:
    for _ in range(seq_length):
        x = np.reshape(starter, (1, len(starter), 1)) / float(len(chars))

        pred_index = np.argmax(model.predict(x))
        starter.append(pred_index)
        starter = starter[1 : len(starter)]

    return starter


def sequence_to_string(seq: np.array, n_to_char: Dict[int, str]) -> str:
    return "".join([n_to_char[value] for value in seq])


if __name__ == "__main__":
    seq_length = 100

    text = load_dataset("data/poems.json")

    chars, n_to_char, char_to_n = create_mapping(text)

    x, X, y = preprocess(text, char_to_n, chars, seq_length)

    model = build_model((X.shape[1], X.shape[2]), y.shape[1])

    # model.fit(X, y, epochs=100, batch_size=50)
    # model.save_weights("weights/weights.h5")

    model.load_weights("weights/weights_epoch_1.h5")

    starter = x[random.randint(0, len(x))]
    print(sequence_to_string(starter, n_to_char))

    for i in range(10):
        starter = generate(starter, seq_length, chars, model)
        print(sequence_to_string(starter, n_to_char))
