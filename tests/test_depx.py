from click.testing import CliRunner

from depx import cli


def test_command_line_interface():
    runner = CliRunner()
    run_result = runner.invoke(cli.main, ['depx/depx.py'])

    assert run_result.exit_code == 0
    assert 'Your report should be available here:' in run_result.output


def test_export():
    runner = CliRunner()
    run_result = runner.invoke(cli.main, ['depx/depx.py', '--export'])

    assert run_result.exit_code == 0
    assert 'Your graph is ready:' in run_result.output
