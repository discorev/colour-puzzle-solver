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
            "-a, --algorithm [BFS|DFS]" in result.output,
            "Options should be shown",
        )
        self.assertTrue(
            "-v, --validate" in result.output, "Options should be shown"
        )
        self.assertTrue(
            "--verbose" in result.output, "Options should be shown"
        )
        self.assertTrue(
            "--help" in result.output, "Help text should be printed"
        )

    def test_cli_bad_puzzle(self):
        """Invoke with a bad puzzle that cannot be solved."""
        runner = CliRunner()
        result = runner.invoke(cli, ["./levels/bad.json"])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Cannot be solved :(" in result.output,
            "This puzzle cannot be solved",
        )

    def test_cli_bad_puzzle_fail_validate(self):
        """Invoke with a bad puzzle that cannot be solved."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--validate", "./levels/bad.json"])

        self.assertEqual(result.exit_code, 2)
        self.assertTrue(
            "Error: Invalid PUZZLE: Invalid colour count" in result.output,
            "This puzzle fails validation",
        )

    def test_cli_bfs_algorithm(self):
        """Invoke with the BFS algorithm and a known puzzle.

        This shoud take 10 moves to solve and results in a known output that
        can be tested for.
        """
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--algorithm=bfs", "./levels/simple_shows_differences.json"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Searching using Breadth-First Search" in result.output,
            "Should show BFS was used for the search",
        )
        self.assertTrue(
            "solved in 10 moves" in result.output,
            "BFS takes 10 moves to solve this puzzle",
        )
        self.assertTrue(
            "(Move(src=0, dest=3), Move(src=0, dest=4), Move(src=1, dest=3), "
            "Move(src=1, dest=4), Move(src=0, dest=1), Move(src=0, dest=3), "
            "Move(src=2, dest=4), Move(src=2, dest=1), Move(src=2, dest=3), "
            "Move(src=2, dest=4))" in result.output,
            "BFS output moves for this puzzle",
        )

    def test_cli_dfs_algorithm(self):
        """Invoke with the DFS algorithm and a known puzzle.

        This shoud take 10 moves to solve and results in a known output that
        can be tested for.
        """
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--algorithm=dfs", "./levels/simple_shows_differences.json"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            "Searching using Depth-First Search" in result.output,
            "Should show DFS was used for the search",
        )
        self.assertTrue(
            "solved in 13 moves" in result.output,
            "DFS takes 13 moves to solve this puzzle",
        )
        self.assertTrue(
            "(Move(src=0, dest=3), Move(src=0, dest=4), Move(src=1, dest=3), "
            "Move(src=1, dest=4), Move(src=0, dest=1), Move(src=0, dest=3), "
            "Move(src=2, dest=0), Move(src=0, dest=4), Move(src=2, dest=0), "
            "Move(src=0, dest=1), Move(src=2, dest=0), Move(src=0, dest=3), "
            "Move(src=2, dest=4))" in result.output,
            "DFS output moves for this puzzle",
        )

    def test_entrypoint(self):
        """Test directly running the module with the help argument.

        This test just validates the return code.
        """
        import subprocess

        result = subprocess.run(
            ["/usr/bin/env", "python3", "-m", "solver", "--help"],
            encoding='ascii',
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(
            "-a, --algorithm [BFS|DFS]" in result.stdout,
            "Options should be shown",
        )
        self.assertTrue(
            "-v, --validate" in result.stdout, "Options should be shown"
        )
        self.assertTrue(
            "--verbose" in result.stdout, "Options should be shown"
        )
        self.assertTrue(
            "--help" in result.stdout, "Help text should be printed"
        )
