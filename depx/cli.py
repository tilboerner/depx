import click
from depx.graph import (
    create_graph_from, to_json, to_html, to_graphml, to_dotfile
)
from depx.parsing import find_imports
import sys


formatters = {
    'json': to_json,
    'html': to_html,
    'graphml': to_graphml,
    'dotfile': to_dotfile
}


@click.command()
@click.argument('path')
@click.option(
    '--format', '-f',
    type=click.Choice(formatters),
    default='json',
    help='Graph output format.'
)
def main(path, format):
    deps = list(find_imports(path))

    if deps:
        graph = create_graph_from(deps)

        export_to = formatters.get(format)
        graph_location = export_to(graph=graph, path=path, dependencies=deps)

        click.echo('Your graph is ready:\n{}'.format(graph_location))

    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
