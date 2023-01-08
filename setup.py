from setuptools import setup

setup(
    name="ttb",
    version="0.0.1",
    packages=["src"],
    entry_points={"console_scripts": ["ttb = src.__main__"]},
)
