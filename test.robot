# Use 4 spaces separator and line_length=80

*** Tasks ***

Different keyword calls
    This is a keyword     fits even with its    # comment

    This is a keyword     fits with its               # comment, but has bad spacing

    This is a keyword       these fit   but        only if you space them correctly

    This is a keyword     these args do not fit       even if you set spacing properly

    This is a keyword     this    last    argument    is    not    really    a # comment

    This is a keyword     these    arguments    wont    fit    with     that   # comment

    This is a keyword     these    arguments    wont    fit    with    or    without    that   # comment
    
    This is a keyword     these     args    have    an    interesting
    ...  # Edge case here                                                        XXX
    ...  More arguments here

    This is a keyword     and     these      are       its     args
    ...    here   are   some    more    args      to      split
    ...    with                irregular                       spacing

    ${assignment}=    This keyword sets the variable   using   these     args

    ${assignment}=    This keyword sets the variable   using   these     args
    ...    here   are   some    more    args      to      split
    ...    with                irregular                       spacing


    This is a keyword     and     these      are       its     args  # Comment

    This is a keyword     and     these      are       its     arg   # Comment
    ...    here   are   some    more    args    to      split        
    ...    with                irregular                       spacing

    This is a keyword     and     these      are       its     arg   # Comment 1
    ...    here   are   some    more    args    to      split        # Comment 2
    ...    with                irregular                     spacing # Comment 3


    ${assignment}=    This keyword sets the variable   using   these  args  # Comment

    ${assignment}=    This keyword sets the variable   using   these     args
    ...    here   are   some    more    args      to      split            # Comment
    ...    with                irregular                       spacing

    ${assignment}=    This keyword sets the variable    # First line comment
    ... using   these     args
    ...    here   are   some    more    args      to      split            # Comment
    ...    with                irregular                       spacing
