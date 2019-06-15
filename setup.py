from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="workfl",
    version="19.6.15.0",  # calver YY.MM.DD.MICRO
    author="Adam Dullage",
    author_email="adam@dullage.com",
    description="A lightweight markup language for simple workflow diagrams.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dullage/workfl",
    license="MIT",
    packages=["workfl"],
)
