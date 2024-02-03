Improved error handling of file related issues (#629)
-----------------------------------------------------

In case Robotidy failed to read or write to file, generic message with decode error was shown. Now it will display
more detailed error message::

    > robotidy read_only_file.robot
    Failed to decode read_only_file.robot with an error: Opening file 'read_only_file.robot' failed:
    PermissionError: [Errno 13] Permission denied: 'read_only_file.robot'
    Skipping file

    0 files reformatted, 1 file left unchanged.
