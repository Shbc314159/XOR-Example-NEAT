#!/usr/bin/env python

from setuptools import setup
from Cython.Build import cythonize

setup(
    name="xor_example_neat",
    version="0.1.0",
    description="XOR Example NEAT implementation",
    author="Shbc314159",
    author_email="",
    ext_modules=cythonize(
        [
            "main.py",
            "Genetic_Algorithm.py",
            "Cube.py",
            "Player.py",
            "Species.py",
            "Walls.py",
            "World.py",
            "barrier.py",
            "graph.py",
            "simulation.py",
            "Neural_Network/*.py"
        ],
        compiler_directives={"language_level": "3"}
    ),
    zip_safe=False,
    install_requires=["Cython"],
)