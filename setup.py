import pathlib

from setuptools import setup

from robotidy.version import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Framework :: Robot Framework
Framework :: Robot Framework :: Tool
Topic :: Software Development :: Testing
Topic :: Software Development :: Quality Assurance
Topic :: Utilities
Intended Audience :: Developers
""".strip().splitlines()

setup(
    name="robotframework-tidy",
    version=__version__,
    description="Code autoformatter for Robot Framework",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MarketSquare/robotframework-tidy",
    author="MarketSquare - Robot Framework community",
    author_email="bartek.hirsz@gmail.com",
    license="Apache License 2.0",
    platforms="any",
    classifiers=CLASSIFIERS,
    keywords="robotframework",
    packages=["robotidy"],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "robotframework>=4.0",
        "click>=7.1.2",
        "colorama>=0.4.3",
        "packaging>=21.0",
        "pathspec>=0.9.0,<0.10.0",
        "tomli>=2.0.0",
        "rich_click==1.4",
    ],
    extras_require={
        "dev": [
            "coverage",
            "invoke",
            "jinja2",
            "pylama_pylint",
            "pylama",
            "pytest",
            "pre-commit",
        ],
        "doc": [
            "sphinx_rtd_theme",
            "sphinx",
            "sphinx-tabs==3.3.1",
            "sphinx-copybutton==0.3.3",
        ],
    },
    entry_points={"console_scripts": ["robotidy=robotidy.cli:cli"]},
)
