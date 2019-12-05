#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.utils import np_utils
import numpy as np


class Baudelaire:
    """
    A text generator trained over Baudelaire's poems.
    """

    def __init__(
        self, dataset_path: str = "data/poems.json", sequence_length: int = 100
    ):
        self.sequence_length = sequence_length
        self._load_dataset(dataset_path)
        self._create_character_number_mapping()
        self._preprocess()
        self._build_model()

    def _load_dataset(self, path: str):
        with open(path, "r") as file:
            poems = json.load(file)
            self.corpus = (
                "\n".join(["\n".join(poem["text"]) for poem in poems]).strip().lower()
            )

    def _create_character_number_mapping(self):
        self.characters = sorted(list(set(self.corpus)))
        self.number_to_character = {n: char for (n, char) in enumerate(self.characters)}
        self.character_to_number = {char: n for (n, char) in enumerate(self.characters)}

    def _preprocess(self):
        sequences, labels = [], []

        for i in range(len(self.corpus) - self.sequence_length):
            sequences.append(
                [
                    self.character_to_number[character]
                    for character in self.corpus[i : i + self.sequence_length]
                ]
            )
            labels.append(
                self.character_to_number[self.corpus[i + self.sequence_length]]
            )

        self.sequences = sequences
        self.normalized_sequences = np.reshape(
            self.sequences, (len(self.sequences), self.sequence_length, 1)
        ) / float(len(self.characters))

        self.labels = np_utils.to_categorical(labels)

    def _build_model(self):
        self.model = Sequential()

        self.model.add(
            LSTM(
                400,
                input_shape=(
                    self.normalized_sequences.shape[1],
                    self.normalized_sequences.shape[2],
                ),
                return_sequences=True,
            )
        )
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(400))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(self.labels.shape[1], activation="softmax"))

        self.model.compile(loss="categorical_crossentropy", optimizer="adam")

    def _sequence_to_string(self, sequence: np.array) -> str:
        return "".join([self.number_to_character[value] for value in sequence])

    def train(self, epochs: int = 1, batch_size: int = 100, save_weights: bool = False):
        self.model.fit(
            self.sequences, self.labels, epochs=epochs, batch_size=batch_size
        )

        if save_weights:
            self.model.save_weights(f"weights/weights_{epochs}_{batch_size}.h5")

    def load_weights(self, path: str = "weights/weights.h5"):
        self.model.load_weights(path)

    def generate(self, starting_sequence: np.array) -> np.array:
        for _ in range(self.sequence_length):
            predicted_character = np.argmax(
                self.model.predict(
                    np.reshape(starting_sequence, (1, len(starting_sequence), 1))
                    / float(len(self.characters))
                )
            )

            starting_sequence.append(predicted_character)
            starting_sequence = starting_sequence[1 : len(starting_sequence)]

        return starting_sequence

    def generate_lines(self, lines_number: int) -> str:
        starting_sequence = self.sequences[random.randint(0, len(self.sequences))]
        output = self._sequence_to_string(starting_sequence) + "\n"

        for _ in range(lines_number):
            starting_sequence = self.generate(starting_sequence)
            output += self._sequence_to_string(starting_sequence)

        return output


def write_to_file(
    contents: str, path: str = "poem.txt",
):
    with open(path, "w") as file:
        file.write(contents)
