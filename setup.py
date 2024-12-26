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
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
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
    python_requires=">=3.8",
    install_requires=[
        "robotframework>=4.0,<7.2",
        "click==8.1.*",
        "colorama>=0.4.3,<0.4.7",
        "pathspec>=0.9.0,<0.12.2",
        "tomli>=2.0,<2.3",
        "rich_click>=1.4,<1.8.6",
        "jinja2>=3.1.3,<4.0",
    ],
    extras_require={
        "dev": [
            "coverage",
            "invoke",
            "jinja2",
            "packaging>=21.0",
            "pyflakes>=2.4,<3.3",
            "pylama",
            "pytest",
            "pre-commit",
            "tomli_w>=1.0,<1.2",
        ],
        "doc": [
            "sphinx",
            "furo",
            "sphinx-design",
            "sphinx-copybutton==0.5.2",
        ],
        "generate_config": ["tomli_w>=1.0,<1.2"],
    },
    entry_points={"console_scripts": ["robotidy=robotidy.cli:cli"]},
)
