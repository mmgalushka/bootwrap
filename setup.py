"""
Bootwrap setup script.
"""

import setuptools

from bootwrap import __version__


def get_long_description():
    """Reads the long project description from the 'README.md' file."""
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="bootwrap",
    version=__version__,
    author="Mykola Galushka",
    author_email="mm.galushka@gmail.com",
    description="Package for rapid development of web-based user interfaces.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmgalushka/bootwrap",
    project_urls={
        "Bug Tracker": "https://github.com/mmgalushka/bootwrap/issues",
    },
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where=".", exclude=["tests"]),
    python_requires=">=3.6",
)
