import click
from depx.graph import create_graph_from, to_json, to_html, to_graphml, to_dotfile
from depx.parsing import find_imports, filter_top_level_names
import sys


formatters = {
    'json': to_json,
    'html': to_html,
    'graphml': to_graphml,
    'dot': to_dotfile,
}


@click.command()
@click.argument('path')
@click.option(
    '--format',
    '-f',
    type=click.Choice(formatters),
    default='json',
    help='Graph output format.',
)
@click.option(
    '--short-names/--no-short-names',
    '-s/ ',
    default=False,
    help='Use the top-level name only for all dependencies (up to first).',
)
def main(path, **kwargs):
    to_format = kwargs['format']
    short_names = kwargs['short_names']
    deps = list(find_imports(path))

    if short_names:
        deps = filter_top_level_names(deps)
    deps = list(deps)

    if deps:
        graph = create_graph_from(deps)

        export_to = formatters.get(to_format)
        click.echo(export_to(graph=graph, path=path, dependencies=deps))

    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
