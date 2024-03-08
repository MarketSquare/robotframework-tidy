SplitTooLongLine fails with fatal exception when splitting invalid keyword (#659)
----------------------------------------------------------------------------------

``SplitTooLongLine`` did not handle invalid syntax where keyword name was omitted::
    Keyword
        ${arg}    ${second_arg}
        ...    ${third_arg}

Such syntax will now be ignored and will not cause fatal exception.
