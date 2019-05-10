from click.testing import CliRunner
import pytest

from depx import cli


fake_module = 'tests/fake_project/fake_module'


def test_command_line_interface():
    runner = CliRunner()
    run_result = runner.invoke(cli.main, [fake_module])

    assert run_result.exit_code == 0


@pytest.mark.parametrize('format,message', [
    ('html', 'Your report should be available here:'),
    ('graphml', 'Your graph is ready:'),
    ('dotfile', 'Your graph is ready:'),
])
def test_export_to(format, message):
    runner = CliRunner()
    run_result = runner.invoke(cli.main, [fake_module, '--format', format])

    assert run_result.exit_code == 0
    assert message in run_result.output
