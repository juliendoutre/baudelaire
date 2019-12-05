#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from baudelaire import Baudelaire, write_to_file

if __name__ == "__main__":
    baudelaire = Baudelaire()
    baudelaire.load_weights(path="weights/weights1.h5")
    write_to_file(baudelaire.generate_lines(10))
