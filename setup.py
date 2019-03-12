from setuptools import setup, find_packages

setup(
    name="quickstart",
    version="0.1.0",
    packages=find_packages(),  # Required
    install_requires=[
        "undictify",
        "requests",
        "flask",
        "flask-jwt-extended",
        "flask-jwt",
        "pyjwt",
        "humanize",
    ],
)
