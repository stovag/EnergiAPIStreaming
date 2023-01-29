"""Script for setting up the witsidedev Package"""
from setuptools import find_packages, setup

print(find_packages())

setup(
    name="energy_den",
    packages=find_packages(),
    version="0.1",
    description="Sample ETL system using data from EnergiAPI",
    author="Evangelos Stogiannos, Theocharis Panagiotis Charalampidis",
    install_requires=["requests", "pytest", "kafka-python"],
)
