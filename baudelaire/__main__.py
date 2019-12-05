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
        "-e",
        "--epochs",
        type=int,
        help="Number of epochs to train the model on",
        default=1,
    )
    train_parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        help="Size of the batches given to the model during the training",
        default=100,
    )
    train_parser.add_argument(
        "-s",
        "--sequence_length",
        type=int,
        help="Length of the characters sequence to consider",
        default=100,
    )
    train_parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to save the weights to",
        default="weights.h5",
    )

    generate_parser = subparsers.add_parser(
        "write", help="Generate some poetry based on your model or the default one"
    )
    generate_parser.add_argument(
        "-n",
        "--sequences",
        type=int,
        help="Number of sequences to generate",
        default=1,
    )
    generate_parser.add_argument(
        "-o", "--output", type=str, help="Path to which to save the output",
    )
    generate_parser.add_argument(
        "-i", "--input", type=str, help="Path to weights to load to the model",
    )
    generate_parser.add_argument(
        "-s",
        "--sequence_length",
        type=int,
        help="Length of the characters sequence to consider",
        default=100,
    )

    args = parser.parse_args()

    baudelaire = Baudelaire(sequence_length=args.sequence_length)

    cmd = args.cmd
    if cmd == "train":
        baudelaire.train(
            args.output, epochs=args.epochs, batch_size=args.batch_size,
        )

    elif cmd == "write":
        baudelaire = Baudelaire(sequence_length=args.sequence_length)

        if args.input is None:
            baudelaire.load_weights()
        else:
            baudelaire.load_weights(args.input)

        output = baudelaire.generate_lines(args.sequences)

        if args.output is None:
            print(output)
        else:
            write_to_file(output, path=args.output)

    else:
        raise parser.error(f"Invalid command {cmd}")


if __name__ == "__main__":
    main()
