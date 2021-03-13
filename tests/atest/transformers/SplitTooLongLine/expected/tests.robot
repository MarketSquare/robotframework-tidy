# Use 4 spaces separator and line_length=80

*** Tasks ***

Different keyword calls
    This is a keyword     fits even with its    # comment

    # comment, but has bad spacing
    This is a keyword
    ...    fits with its

    This is a keyword
    ...    these fit
    ...    but
    ...    only if you space them correctly

    This is a keyword
    ...    these args do not fit
    ...    even if you set spacing properly

    This is a keyword
    ...    this
    ...    last
    ...    argument
    ...    is
    ...    not
    ...    really
    ...    a # comment

    # comment
    This is a keyword
    ...    these
    ...    arguments
    ...    wont
    ...    fit
    ...    with
    ...    that

    # comment
    This is a keyword
    ...    these
    ...    arguments
    ...    wont
    ...    fit
    ...    with
    ...    or
    ...    without
    ...    that
    
    # Edge case here →→→→→→→→→→→→→→→→                                    HERE
    This is a keyword
    ...    these
    ...    args
    ...    have
    ...    an
    ...    interesting
    ...    
    ...    More arguments here

    This is a keyword     and     these      are       its     args
    ...    here   are   some    more    args      to      split
    ...    with                irregular                       spacing

    ${assignment}=    This keyword sets the variable   using   these     args

    ${assignment}=    This keyword sets the variable   using   these     args
    ...    here   are   some    more    args      to      split
    ...    with                irregular                       spacing


    This is a keyword     and     these      are       its     args  # Comment

    This is a keyword     and     these      are       its     arg   # Comment
    ...    here   are   some    more    args
    ...    with                irregular                       spacing

    # Comment 1
    # Comment 2
    This is a keyword
    ...    and
    ...    these
    ...    are
    ...    its
    ...    arg
    ...    here
    ...    are
    ...    some
    ...    more
    ...    args
    ...    with
    ...    irregular
    ...    spacing # Not really a comment


    # Comment
    ${assignment}=    This keyword sets the variable
    ...    using
    ...    these
    ...    args

    # Comment
    ${assignment}=    This keyword sets the variable
    ...    using
    ...    these
    ...    args
    ...    here
    ...    are
    ...    some
    ...    more
    ...    args
    ...    to
    ...    split
    ...    with
    ...    irregular
    ...    spacing


Newlines
    Keyword

    # Newlines with trailing space are not changed
        
        

    Keyword
