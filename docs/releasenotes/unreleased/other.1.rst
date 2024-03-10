File disablers in Comments section (#587)
-----------------------------------------

Previously file formatting disablers were only recognized if they were placed in the first line of file::

    # robotidy: off
    *** Settings ***

Now Robotidy will acknowledge any disabler in the first comment section (with or without header)::

    Following line disables formatting of this file with Robotidy
   # robotidy: off

   *** Settings ***

Or::

    *** Comments ***
    # robotidy: off

   *** Test Cases ***
