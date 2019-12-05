#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from .baudelaire import Baudelaire, write_to_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A text generator trained over Baudelaire's poems"
    )

    subparsers = parser.add_subparsers(help="Available commands", dest="cmd")

    train_parser = subparsers.add_parser(
        "train", help="Train the model with chosen parameters"
    )
    train_parser.add_argument(
        "-e", "--epochs", type=int, help="Number of epochs to train the model on"
    )
    train_parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        help="Size of the batches given to the model during the training",
    )
    train_parser.add_argument(
        "-s",
        "--sequence_length",
        type=int,
        help="Length of the characters sequence to consider",
    )
    train_parser.add_argument(
        "-o", "--output", type=str, help="Path to save the weights to",
    )

    generate_parser = subparsers.add_parser(
        "write", help="Generate some poetry based on your model or the default one"
    )
    generate_parser.add_argument(
        "-s", "--sequences", type=int, help="Number of sequences to generate",
    )
    generate_parser.add_argument(
        "-o", "--output", type=str, help="Path to which save the output",
    )
    generate_parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to weights to load to configure the model",
    )
    generate_parser.add_argument(
        "-s",
        "--sequence_length",
        type=int,
        help="Length of the characters sequence to consider",
    )

    cmd = parser.parse_args().cmd
    if cmd == "train":
        train_parser.parse_args()
    elif cmd == "write":
        generate_parser.parse_args()
    else:
        raise parser.error(f"Invalid command {cmd}")

    baudelaire = Baudelaire()
    baudelaire.load_weights(
        path=os.path.join(os.path.dirname(__file__), "weights/weights1.h5")
    )

    write_to_file(baudelaire.generate_lines(10))


if __name__ == "__main__":
    main()
