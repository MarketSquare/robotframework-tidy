Gitignore patterns incorrectly matching paths (#632)
----------------------------------------------------

Robotidy loads the ``.gitignore`` files to not format ignored files and directories. There was a bug with how the paths
are resolved which leaded to Robotidy ignoring too many paths. For example given project at ``/tmp/a/b/c/d/my-project``
path, if ``.gitignore`` file contained ``tmp/`` pattern it matched whole project (``/tmp/a/b/c/d/my-project``)
instead of path relative to project root (``/tmp/a/b/c/d/my-project/tmp/``).

Now Robotidy resolve paths correctly and such paths should be handled correctly.
