from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ttlcollections",
    version="1.0",
    author="Nocturn9x",
    author_email="nocturn9x@intellivoid.net",
    description="Pure python collections with TTL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nocturn9x/ttlqueue",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3.0"
    ],
    python_requires='>=3.6',
)
