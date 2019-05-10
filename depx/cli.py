import click
from depx.graph import create_from, export_to
from depx.parsing import find_imports
import json
import sys


@click.command()
@click.argument('path')
@click.option('--format', '-f', help='Export your graph to: html, graphml or dotfile.')
def main(path, format):
    deps = list(find_imports(path))

    if deps:
        G = create_from(deps)
        graph_location = export_to(G, format, path)

        if format == 'html':
            click.echo('Your report should be available here: {}'.format(graph_location))
        elif format == 'graphml':
            click.echo('Your graph is ready: {}'.format(graph_location))
        elif format == 'dotfile':
            click.echo('Your graph is ready: {}'.format(graph_location))
        else:
            click.echo(json.dumps(deps, indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
