from setuptools import setup, find_packages

setup(
    name="tfmig",
    version="0.1",
    packages=find_packages(),
    author="Lívia Almeida Barbosa",
    description="This project is the backend of an application used to "
                "detect commits that migrate unittest to pytest in Python repositories",
    url="https://github.com/liviaab/tfmig",
)
