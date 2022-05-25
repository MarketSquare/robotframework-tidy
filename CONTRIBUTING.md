Contribution guideline
======================

Getting started
----------------
Did you spot a bug or you really want to see some feature implemented? It's always best to start with creating issue in GitHub.
It doesn't matter if you're actually willing to make change on your own. Creating issue allow us to discuss proposed changes (
and cover possible edge cases) and also prevents multiple people from working on the same problem.

You can also start discussion in our slack channel: [#tidy](https://robotframework.slack.com/archives/C01FR5992N6).

Setup
------
Create your own fork of Robotidy first (instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo)). 
It will be easier to create Pull Requests later with your own fork. After cloning your fork to your disk install Robotidy
from the source code with `dev` profile. Run following in the root of the project:
```
pip install -e .[dev,rich]
```
Option `-e` allows changes done by you to be automatically reloaded without need for reinstalling the package.
`dev` profile installs extra libraries useful for testing and scripting (such as pytest or invoke).
`rich` profile provide prettified console outputs.

Other dependencies
-------------------
For running our utility scripts and test environments following Python packages are needed:

- invoke
- nox

Creating new transformer
------------------------
When you want to add new a transformer to Robotidy you can use `add-transformer` invoke helper script. It will create stub
classes and tests. To do this run following command in the project root:
```
invoke add-transformer TRANSFORMER-NAME
```
It will create `TRANSFORMER-NAME.py` file in transformer directory with class stub and it will also create initial structure 
inside `tests/atest/transformers` directory. Additionally, it will add name of your transformer to `robotidy/transformers/__init__.py file` to 
TRANSFORMERS lists. This list determines the order of transformers that will be run. There are transformers that affect the others but if 
you're not sure how your transformer will work with others just leave the default order.

If you don't want to run your transformer with default ones (so it could be run only when selected with 
`--transform` or configured with `enabled=True`) add the following flag to invoke script:
```
invoke add-transformer TRANSFORMER-NAME --disabled
```

Helper script will also add `docs/source/transformers/TRANSFORMER-NAME.rst` file. You can add full documentation 
of your transformer together with more usage examples and possible configurations. Refer to other transformers documentation 
for used syntax (our documentation engine use sphinx under the hood with alabaster theme and sphinx_tabs.tabs plugin). Documentation 
will be rendered on merge with the master branch, but you can generate your local version using `make.bat` script in docs directory.

Robotidy uses Robot Framework Parsing API for visiting robot source files (parsed as AST trees). Visit [this](https://robot-framework.readthedocs.io/en/master/autodoc/robot.api.html#module-robot.api.parsing) 
page to learn more. You can modify visited node (for example change the value of the node or replace some of the child tokens). 
Transformers inherit from `ModelTransform` parent class that requires you to return node from visitor method - if you return None 
it will remove node from your file. 

See examples of creating external transformer [here](https://robotidy.readthedocs.io/en/latest/external_transformers.html). The same logic 
can be used for internal transformers.

Testing
--------
See ``tests/README.rst`` file for more information on testing.

Other contributions
-------------------
All contributions are welcome. If you're changing the source code remember to add tests - see `tests/README.md` for more information. 
If you're not sure how to add tests to your changes then don't worry and contact us either through GitHub issues or Slack channel 
([#tidy](https://robotframework.slack.com/archives/C01FR5992N6)) - we will help you :). 