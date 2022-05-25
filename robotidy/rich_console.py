try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table
    RICH_SUPPORTED = True
except ImportError:
    RICH_SUPPORTED = False
    import re
    import click


if RICH_SUPPORTED:
    console = Console()
else:
    class Console:
        @staticmethod
        def print(msg):
            msg = re.sub(r"\[[^\]]+\]", "", str(msg))
            click.echo(msg)

    class Markdown:
        def __init__(self, documentation, **kwargs):
            self.documentation = documentation

        def __str__(self):
            return self.documentation

    class Table:
        def __init__(self, *args, title, **kwargs):
            self.title = title
            self.columns = []
            self.rows = []

        def add_column(self, name, **kwargs):
            self.columns.append(name)

        def add_row(self, *args):
            self.rows.append([*args])

        def __str__(self):
            s = f"{self.title: ^40}\n"
            for col in self.columns:
                s += f"{col: <35}"
            s += "\n"
            for row in self.rows:
                for col in row:
                    s += f"{col: <35}"
                s += "\n"
            return s

    console = Console()
