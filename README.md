![Codecov](https://img.shields.io/codecov/c/github/MarketSquare/robotframework-tidy/main "Code coverage on master branch")
![PyPI](https://img.shields.io/pypi/v/robotframework-tidy?label=version "PyPI package version")
![Python versions](https://img.shields.io/pypi/pyversions/robotframework-tidy "Supported Python versions")
![Licence](https://img.shields.io/pypi/l/robotframework-tidy "PyPI - License")

---

<img style="float:right" src="https://raw.githubusercontent.com/MarketSquare/robotframework-tidy/main/docs/source/_static/robotidy_logo_small.png">

Robotidy
===============
- [Introduction](#introduction)
- [Documentation](#documentation)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

Introduction <a name="introduction"></a>
------------
Robotidy is a tool for autoformatting Robot Framework code.

It is spiritual descendant of Robot Framework's internal robot.tidy package.

Documentation <a name="documentation"></a>
-------------
Full documentation available [here](https://robotidy.readthedocs.io). :open_book:

Requirements <a name="requirements"></a>
------------

Python 3.8+ :snake: and Robot Framework 4.0.0+ :robot:.

Installation <a name="installation"></a>
------------

You can install Robotidy simply by running:
```
pip install -U robotframework-tidy
```

Usage <a name="usage"></a>
-----
Call robotidy with path(s) to file/directory with robot files:

```
robotidy tests
robotidy test.robot
robotidy tests/resources test.robot
```
    
All command line options can be displayed in help message by executing:

```
robotidy --help
```

See [documentation](https://robotidy.readthedocs.io/en/latest/configuration/index.html) for information how to configure 
robotidy.

Example <a name="example"></a>
-------
Ugly code before transforming with robotidy:
```robotframework
*** Settings ***
Force Tags  tags  tag2
Library  Collections
Resource  important.robot
Library   MyCustomLibrary.py

Test Setup  Setup Keyword


*** test case*
Test1
    [ teardown]  Teardown Keyword
    Keyword
    FOR  ${var}  IN RANGE  10
    Run Keyword If  ${var}>5  Other Keyword
    END
*** Variables ***
${var}=  2
${bit_longer}  10
${var2}   a
...  b

*** Keywords ***

```
A lot prettier code after:
```robotframework
*** Settings ***
Library         Collections
Library         MyCustomLibrary.py
Resource        important.robot

Test Setup      Setup Keyword

Force Tags      tags    tag2

*** Variables ***
${var}              2
${bit_longer}       10
${var2}             a
...                 b

*** Test Cases ***
Test1
    Keyword
    FOR    ${var}    IN RANGE    10
        IF    ${var}>5
            Other Keyword
        END
    END
    [Teardown]    Teardown Keyword

```
