import os
import sys

import setuptools


def read_file(file):
    with open(os.path.join(os.path.dirname(__file__), file)) as readable:
        return readable.read()


README = read_file("README.md")

setuptools.setup(
    name="ProgettiHWSW",
    version="0.1.3",
    long_description="\n\n".join([README]),
    long_description_content_type="text/markdown",
    description="Controls ProgettiHWSW relay boards.",
    url="http://github.com/ardaseremet/progettihwsw",
    download_url="http://github.com/ardaseremet/progettihwsw/tarball/0.1.3",
    author="Arda Seremet",
    author_email="ardaseremet@outlook.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["aiohttp", "lxml"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Telecommunications Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Legal Industry",
    ],
)
