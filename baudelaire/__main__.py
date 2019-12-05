#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .baudelaire import Baudelaire, write_to_file


def main():
    baudelaire = Baudelaire()
    baudelaire.load_weights(
        path=os.path.join(os.path.dirname(__file__), "weights/weights1.h5")
    )
    write_to_file(baudelaire.generate_lines(10))


if __name__ == "__main__":
    main()
