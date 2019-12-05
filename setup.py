#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="baudelaire",
    description="A tool to automatically generate poems in Baudelaire's style",
    url="https://github.com/juliendoutre/baudelaire",
    author="Julien Doutre",
    author_email="jul.doutre@gmail.com",
    license="MIT",
    version="0.1.0",
    packages=["baudelaire"],
    # install_requires=["numpy", "keras" "tensorflow"],
    entry_points={"console_scripts": ["baudelaire = baudelaire.__main__:main"]},
    zip_safe=False,
    include_package_data=True,
)
