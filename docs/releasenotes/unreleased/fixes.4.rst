Variables in tags should be renamed with RenameVariables (#641)
---------------------------------------------------------------

Variables defined in the ``[Tags]`` should be now handled by ``RenameVariables`` transformer. Following code::

    Test case
        [Tags]    tag with ${variable}
        Test Step

should now (with the default configuration) be transformed to::

    Test case
        [Tags]    tag with ${VARIABLE}
        Test Step
