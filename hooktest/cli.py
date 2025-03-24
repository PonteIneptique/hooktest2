from typing import List
from .tester import Tester, Log
import click
import tabulate


def to_small_caps(text):
    small_caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    )
    return text.translate(small_caps_map)


class CustomLogger:
    def __init__(self, level: str = "minimal"):
        """

        minimal
        verbose

        """
        self._eq = {
            "minimal": 10, # Only bugs and necessary info is shown
            "details": 5,  # Some information is kept
            "verbose": 0   # Everything is shown
        }
        self.level = self._eq[level]

    def _print(self, string, level: str = "minimal", indent: int = 0, color : str = None, **kwargs):
        if self._eq[level] >= self.level:
            click.echo(click.style(indent*"\t"+string, fg=color, **kwargs))

    def header(self, string, level: str = "minimal"):
        self._print(f"\n==== {to_small_caps(string.title())} ====", level=level, bold=True)

    def info(self, string, level: str = "minimal", indent: int = 0):
        self._print(f"INFO: {string}", level=level, indent=indent, color="cyan")

    def filter_logs(self, content: List[Log]):
        return [
            f"{log.name}: {self.green_red(log.details or "✔", log.status)}"
            for log in content
            if log.status == False or self.level <= 0
        ]

    def filter_append(self, haystack: List, hay, level: str = "minimal"):
        if self._eq[level] >= self.level:
            haystack.append(hay)

    def green_red(self, string: str, status):
        if not status:
            return click.style(string, fg="red")
        elif status and self.level <= 5:  # Only show green in details / verbose
            return click.style(string, fg="green")
        return string

    def checkmark(self, status):
        if status:
            return self.green_red("✔", status)
        return self.green_red("✗", status)

@click.command
@click.argument("files", nargs=-1, type=click.Path(file_okay=True, dir_okay=False, exists=True))
def cli(files):
    tester = Tester()
    printer = CustomLogger("verbose")
    count_collections, count_resources = tester.ingest(files)

    printer.info(f"Found {count_collections} collection(s)")
    printer.info(f"Found {count_resources} resource(s)")

    printer.header("Report: Catalog files")

    table = [["File", "Status", "Tests"]]

    for file, result in tester.results.items():
        printer.filter_append(
            haystack=table,
            hay=[
                file,
                printer.checkmark(result.status),
                "\n".join(printer.filter_logs(result.statuses))
            ],
            level="minimal"
        )

    click.echo(tabulate.tabulate(table, tablefmt="grid"))


if __name__ == "__main__":
    cli()