"""Tests for the main CLI."""
from unittest import TestCase
from click.testing import CliRunner
from solver.cli.main import cli


class TestCli(TestCase):
    """Unit test cases for the solver cli."""

    def test_cli_no_arguments(self):
        """Invoke with no arguments and assert an error is raised."""
        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 2)
        self.assertTrue(
            "Missing argument 'PUZZLE'." in result.output,
            "Required arguments must be present to run cli",
        )

    def test_cli_help(self):
        """Invoke with the help flag and assert that help test is printed."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "--help" in result.output, "Help text should be printed"
        )
        self.assertTrue(
            "-v, --verbose" in result.output, "Options should be shown"
        )
