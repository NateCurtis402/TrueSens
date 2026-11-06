# Tests for main.py, run as a subprocess, standard library only (unittest)
import re
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN = PROJECT_ROOT / "main.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )


class TestCli(unittest.TestCase):

    def test_list_shows_five_games(self):
        result = run_cli("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), 5)
        for name in ("Valorant", "Counter-Strike 2", "Apex Legends", "Overwatch 2", "Marvel Rivals"):
            self.assertIn(name, result.stdout)

    def test_convert_cs2_to_valorant_by_alias(self):
        result = run_cli("--dpi", "1600", "--sens", "1.0", "--from", "cs2", "--to", "val")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Valorant", result.stdout)
        self.assertIn("0.31", result.stdout)

    def test_convert_without_to_prints_cm360(self):
        result = run_cli("--dpi", "1600", "--sens", "1.0", "--from", "cs2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("26.0 cm", result.stdout)

    def test_cm360_to_overwatch_prints_positive_number(self):
        result = run_cli("--dpi", "1600", "--cm360", "30", "--to", "ow2")
        self.assertEqual(result.returncode, 0, result.stderr)
        match = re.search(r"Overwatch 2:\s*(-?\d+(?:\.\d+)?)", result.stdout)
        self.assertIsNotNone(match, result.stdout)
        self.assertGreater(float(match.group(1)), 0)

    def test_unknown_game_exits_1_without_traceback(self):
        result = run_cli("--dpi", "1600", "--sens", "1.0", "--from", "notagame")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("Available games", result.stderr)

    def test_missing_required_args_exits_2(self):
        result = run_cli("--sens", "1.0", "--from", "cs2")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
