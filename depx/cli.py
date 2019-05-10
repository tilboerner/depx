import click
from depx.graph import create_from, export_to, report
from depx.parsing import find_imports, filter_top_level_names
import json
import sys


@click.command()
@click.argument('path')
@click.option("--export", "-e", is_flag=True, help="Export your graph to a file.")
@click.option("--full-names", "-f", is_flag=True, help="")  # FIXME help
def main(path, export, *, full_names):
    deps = find_imports(path)
    if not full_names:
        deps = filter_top_level_names(deps)
    deps = list(deps)

    if deps:
        click.echo(json.dumps(deps, indent=4))
        G = create_from(deps)

        report_location = report(G, path)
        click.echo("Your report should be available here: {}".format(report_location))
        if export:
            filename = export_to(G, export)
            click.echo("Your graph is ready: {}".format(filename))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
