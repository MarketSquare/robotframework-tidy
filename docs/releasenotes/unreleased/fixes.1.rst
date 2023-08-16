Robot Framework 6.1 fixes (#550)
--------------------------------

- ``Translate`` transformer should now properly handle creating Comments section (if needed),
- Missing settings translations should now be ignored by ``Translate`` transformer,
- Files with invalid sections (for example unrecognized translated section names) should be ignored by
  ``MergeAndOrderSections``
