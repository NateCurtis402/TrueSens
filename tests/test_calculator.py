# Tests for calculator.py, standard library only (unittest)
import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from calculator import cm360_to_sensitivity, sensitivity_to_cm360

GAMES_FILE = PROJECT_ROOT / "games.json"

CS2_SENS = 1.0
CS2_YAW = 0.022
DPI = 1600


def load_games():
    with open(GAMES_FILE, encoding="utf-8") as f:
        return json.load(f)["games"]


class TestSensitivityToCm360(unittest.TestCase):

    def test_cs2_reference_value(self):
        # 360 / (0.022 * 1.0) / 1600 * 2.54 = 25.977... cm
        result = sensitivity_to_cm360(1.0, 0.022, 1600)
        self.assertAlmostEqual(result, 25.98, delta=0.01)


class TestRoundTrip(unittest.TestCase):

    CASES = [
        (1.0, 0.022, 1600),
        (2.5, 0.022, 800),
        (0.35, 0.022, 400),
        (0.4, 0.07, 800),
        (0.25, 0.07, 1600),
        (1.2, 0.07, 3200),
    ]

    def test_cm360_round_trip(self):
        for s, yaw, dpi in self.CASES:
            with self.subTest(sensitivity=s, yaw=yaw, dpi=dpi):
                cm = sensitivity_to_cm360(s, yaw, dpi)
                back = cm360_to_sensitivity(cm, yaw, dpi)
                self.assertAlmostEqual(back, s, delta=1e-9)


class TestGamesRoundTrip(unittest.TestCase):

    def test_every_game_round_trips_to_cs2(self):
        games = load_games()
        self.assertTrue(games, "games.json contains no games")
        for game in games:
            with self.subTest(game=game["name"], yaw=game["yaw"]):
                cm = sensitivity_to_cm360(CS2_SENS, CS2_YAW, DPI)
                game_sens = cm360_to_sensitivity(cm, game["yaw"], DPI)

                game_cm = sensitivity_to_cm360(game_sens, game["yaw"], DPI)
                back_to_cs2 = cm360_to_sensitivity(game_cm, CS2_YAW, DPI)

                self.assertAlmostEqual(back_to_cs2, CS2_SENS, delta=1e-9)


if __name__ == "__main__":
    unittest.main()
