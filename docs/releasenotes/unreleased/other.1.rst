More verbose output (#572)
---------------------------

Robotidy output is now more verbose. If the file is formatted (or would be formatted if not for
``--check`` or ``--no-overwrite options) the file path and run summary is displayed:

```
> robotidy --check .
Would reformat  D:\test_repository\resources\db_keywords.resource file
Would reformat D:\test_repository\tests\ui\login.robot file

2 files would be reformatted, 112 files would be left unchanged.
```

```
> robotidy .
Formatting D:\test_repository\resources\db_keywords.resource file
Formatting D:\test_repository\tests\ui\login.robot file

2 files reformatted, 112 files left unchanged.
```

```
> robotidy --verbose .
Found D:\test_repository\resources\ui_keywords.resource file
Found (...)
Formatting D:\test_repository\resources\db_keywords.resource file
Found (...)
Formatting D:\test_repository\tests\ui\login.robot file
Found (...)

2 files reformatted, 112 files left unchanged.
```
