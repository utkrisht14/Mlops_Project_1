from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mlops-project-1",
    version="0.1.0",
    author="Utkrisht",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
)
