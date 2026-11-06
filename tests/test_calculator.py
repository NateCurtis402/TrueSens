# Tests for calculator.py, standard library only (unittest)
import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import calculator
from calculator import (
    cm360_for_sensitivity,
    cm360_to_sensitivity,
    convert_sensitivity,
    find_game,
    sensitivity_for_cm360,
    sensitivity_to_cm360,
)

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


class TestKnownCrossGameValues(unittest.TestCase):

    def game_yaw(self, name):
        for game in load_games():
            if game["name"] == name:
                return game["yaw"]
        self.fail(f"{name} not found in games.json")

    def test_cs2_to_valorant(self):
        # Valorant yaw 0.07: 1.0 * 0.022 / 0.07 = 0.3143
        valorant_yaw = self.game_yaw("Valorant")
        cm = sensitivity_to_cm360(1.0, 0.022, 1600)
        result = cm360_to_sensitivity(cm, valorant_yaw, 1600)
        self.assertAlmostEqual(result, 0.3143, delta=0.001)

    def test_cs2_to_apex_is_one_to_one(self):
        # Apex shares the Source yaw 0.022, so the sensitivity carries over 1:1
        apex_yaw = self.game_yaw("Apex Legends")
        cm = sensitivity_to_cm360(1.0, 0.022, 1600)
        result = cm360_to_sensitivity(cm, apex_yaw, 1600)
        self.assertAlmostEqual(result, 1.0, delta=1e-9)

    def test_all_yaw_values_are_plausible(self):
        games = load_games()
        self.assertTrue(games, "games.json contains no games")
        for game in games:
            with self.subTest(game=game["name"], yaw=game["yaw"]):
                self.assertGreaterEqual(game["yaw"], 0.001)
                self.assertLessEqual(game["yaw"], 0.1)


class TestGameHelpers(unittest.TestCase):

    def setUp(self):
        self.games = calculator.load_games()

    def test_load_games_returns_five_games(self):
        self.assertEqual(len(self.games), 5)

    def test_find_game_is_case_insensitive(self):
        self.assertEqual(find_game("vALORANT", self.games)["name"], "Valorant")
        self.assertEqual(find_game("counter-strike 2", self.games)["name"], "Counter-Strike 2")

    def test_find_game_matches_aliases_case_insensitively(self):
        self.assertEqual(find_game("cs2", self.games)["name"], "Counter-Strike 2")
        self.assertEqual(find_game("VAL", self.games)["name"], "Valorant")
        self.assertEqual(find_game("apex", self.games)["name"], "Apex Legends")
        self.assertEqual(find_game("Ow2", self.games)["name"], "Overwatch 2")
        self.assertEqual(find_game("mr", self.games)["name"], "Marvel Rivals")

    def test_find_game_raises_key_error_on_unknown_name(self):
        with self.assertRaises(KeyError):
            find_game("Not A Real Game", self.games)

    def test_convert_same_game_returns_input_unchanged(self):
        for game in self.games:
            with self.subTest(game=game["name"]):
                result = convert_sensitivity(0.734, game["name"], game["name"], DPI, self.games)
                self.assertEqual(result, 0.734)

    def test_convert_cs2_to_valorant(self):
        result = convert_sensitivity(1.0, "Counter-Strike 2", "Valorant", DPI, self.games)
        self.assertAlmostEqual(result, 0.3143, delta=0.001)

    def test_convert_cs2_to_apex_is_one_to_one(self):
        result = convert_sensitivity(1.0, "Counter-Strike 2", "Apex Legends", DPI, self.games)
        self.assertAlmostEqual(result, 1.0, delta=1e-9)

    def test_every_game_has_https_source(self):
        for game in self.games:
            with self.subTest(game=game["name"]):
                source = game.get("source", "")
                self.assertTrue(source)
                self.assertTrue(source.startswith("https://"))

    def test_cm360_helpers_round_trip_for_every_game(self):
        for game in self.games:
            with self.subTest(game=game["name"]):
                cm = cm360_for_sensitivity(1.0, game["name"], DPI, self.games)
                back = sensitivity_for_cm360(cm, game["name"], DPI, self.games)
                self.assertAlmostEqual(back, 1.0, delta=1e-9)


if __name__ == "__main__":
    unittest.main()
