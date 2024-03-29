#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import warnings
import logging

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.simplefilter(action="ignore", category=FutureWarning)
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.utils import np_utils
import numpy as np


class Baudelaire:
    """
    A text generator trained over Baudelaire's poems.
    """

    def __init__(self, sequence_length: int = 100, verbose: bool = False) -> None:
        self.verbose = verbose
        self.sequence_length = sequence_length
        self._load_dataset(os.path.join(os.path.dirname(__file__), "data/poems.json"))
        self._create_character_number_mapping()
        self._preprocess()
        self._build_model()

    def _load_dataset(self, path: str) -> None:
        if self.verbose:
            logging.info(f"Loading dataset from {path}")

        with open(path, "r") as file:
            poems = json.load(file)
            self.corpus = (
                "\n".join(["\n".join(poem["text"]) for poem in poems]).strip().lower()
            )

    def _create_character_number_mapping(self) -> None:
        self.characters = sorted(list(set(self.corpus)))
        self.number_to_character = {n: char for (n, char) in enumerate(self.characters)}
        self.character_to_number = {char: n for (n, char) in enumerate(self.characters)}

    def _preprocess(self) -> None:
        if self.verbose:
            logging.info(f"Preprocessing {len(self.corpus)} characters")

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

        if self.verbose:
            logging.info(f"{len(self.sequences)} sequences in the corpus")

    def _build_model(self) -> None:
        if self.verbose:
            logging.info("Building the model")

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

        if self.verbose:
            logging.info("Compiling the model")

        self.model.compile(loss="categorical_crossentropy", optimizer="adam")

    def _sequence_to_string(self, sequence: np.array) -> str:
        return "".join([self.number_to_character[value] for value in sequence])

    def train(self, weights_path: str, epochs: int = 1, batch_size: int = 100) -> None:
        if self.verbose:
            logging.info(
                f"Training the model with {epochs} epochs and a {batch_size} batch size"
            )

        self.model.fit(
            self.normalized_sequences, self.labels, epochs=epochs, batch_size=batch_size
        )

        self.model.save_weights(weights_path)

        if self.verbose:
            logging.info(f"Saving weights to {weights_path}")

    def load_weights(
        self, path: str = os.path.join(os.path.dirname(__file__), "data/weights.h5")
    ) -> None:
        if self.verbose:
            logging.info(f"Loading weights from {path}")

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
        if self.verbose:
            logging.info(f"Generating {lines_number} sequences")

        starting_sequence = self.sequences[random.randint(0, len(self.sequences))]
        output = self._sequence_to_string(starting_sequence) + "\n"

        for i in range(lines_number):
            starting_sequence = self.generate(starting_sequence)
            output += self._sequence_to_string(starting_sequence)

            if self.verbose:
                logging.info(f"New sequence generated ({i+1}/{lines_number})")

        return output

    def write_to_file(self, contents: str, path: str = "poem.txt") -> None:
        if self.verbose:
            logging.info(f"Writing output to file {path}")

        with open(path, "w") as file:
            file.write(contents)
