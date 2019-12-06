#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


def init_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
