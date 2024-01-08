Configurable keyword case in RenameKeywords (#585)
---------------------------------------------------

It is now possible to configure how RenameKeywords capitalize keywords with ``keyword_case`` parameter:

- keyword_case = ``capitalize_words`` (default) - capitalize each word
- keyword_case = ``capitalize_first`` (default) - only capitalize first character
- keyword_case = ``ignore`` (default) - do not change existing case
