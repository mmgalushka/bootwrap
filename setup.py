"""
Bootwrap setup script.
"""

import setuptools


def get_long_description():
    """Reads the long project description from the 'README.md' file."""
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


def local_scheme(version):
    return ''


setuptools.setup(
    name="bootwrap",
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
    # use_scm_version={'version_scheme': 'guess-next-dev',
    #                  'local_scheme': 'no-local-version'},
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=['setuptools_scm']
)
