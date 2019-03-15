# -*- coding: utf-8 -*-

"""Console script for depx."""
import sys
import click


@click.group()
def main():
    return 0


@main.command()
@click.argument('path')
def parse(path):
    import json
    from depx.parsing import find_imports
    deps = list(find_imports(path))
    click.echo(json.dumps(deps, indent=4))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
