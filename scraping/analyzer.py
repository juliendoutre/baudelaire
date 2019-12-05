#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Analyzer:
    """
    A statistics computer about the dataset.
    """

    def __init__(self, path: str):
        self._load_dataset(path)

    def _load_dataset(self, path: str):
        with open(path, "r") as f:
            self.dataset = json.load(f)

    def compute_statistics(self):
        self.statistics = {
            "poems": {},
            "collections": {},
            "lines": 0,
            "characters": 0,
        }

        for poem in self.dataset:
            if poem["collection"] in self.statistics["collections"]:
                self.statistics["collections"][poem["collection"]]["poems"] += 1
            else:
                self.statistics["collections"][poem["collection"]] = {
                    "poems": 1,
                    "lines": 0,
                    "characters": 0,
                }

            self.statistics["poems"][poem["title"]] = {
                "lines": len(poem["text"]),
                "characters": 0,
            }

            for line in poem["text"]:
                self.statistics["collections"][poem["collection"]]["lines"] += 1
                self.statistics["lines"] += 1

                for _ in line:
                    self.statistics["characters"] += 1
                    self.statistics["collections"][poem["collection"]][
                        "characters"
                    ] += 1
                    self.statistics["poems"][poem["title"]]["characters"] += 1

        self.statistics["collections"]["number"] = len(self.statistics["collections"])
        self.statistics["poems"]["number"] = len(self.statistics["poems"])

    def save_to_file(self, path: str):
        with open(path, "w") as f:
            json.dump(self.statistics, f)


if __name__ == "__main__":
    analyzer = Analyzer("data/poems.json")
    analyzer.compute_statistics()
    analyzer.save_to_file("data/stats.json")
