from click.testing import CliRunner
import pytest

import depx
from depx import cli


fake_module = 'tests/fake_project/fake_module'


def test_package_version_matches_project():
    import pkg_resources
    assert depx.__version__ == pkg_resources.get_distribution('depx').version


def test_command_line_interface():
    runner = CliRunner()
    run_result = runner.invoke(cli.main, [fake_module])

    assert run_result.exit_code == 0


@pytest.mark.parametrize('format', [
    'json', 'html', 'graphml', 'dot'
])
def test_export_to(format):
    runner = CliRunner()
    run_result = runner.invoke(cli.main, [fake_module, '--format', format])

    assert run_result.exit_code == 0
