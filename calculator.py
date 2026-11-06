import json
from pathlib import Path

# Math Function, calculation for sens to cm360
def sensitivity_to_cm360(sensitivity, yaw, dpi):
    
# Math Function, calculation for cm360
    counts_per_360 = 360 / (yaw * sensitivity)
    inches_per_360 = counts_per_360 / dpi
    cm_per_360 = inches_per_360 * 2.54

    result = cm_per_360
    return result

#Math Function, calculation for cm360 to sens
def cm360_to_sensitivity(cm360, yaw, dpi):

    inches360 = cm360/ 2.54
    counts360 = inches360 * dpi
    sensitivity = 360 / (counts360 * yaw)

    result = sensitivity
    return result


GAMES_FILE = Path(__file__).resolve().parent / "games.json"


def load_games(path=None):
    """Read games.json (repo root by default) and return the list of game dicts."""
    games_path = Path(path) if path is not None else GAMES_FILE
    with open(games_path, encoding="utf-8") as f:
        return json.load(f)["games"]


def find_game(name, games):
    """Return the game dict whose name or alias matches case-insensitively, else raise KeyError."""
    wanted = name.strip().lower()
    for game in games:
        names = [game["name"], *game.get("aliases", [])]
        if wanted in (n.lower() for n in names):
            return game
    available = ", ".join(game["name"] for game in games)
    raise KeyError(f"Unknown game {name!r}. Available games: {available}")


def cm360_for_sensitivity(sensitivity, game, dpi, games):
    """In-game sensitivity at dpi (counts per inch) -> cm per 360 degrees for game."""
    return sensitivity_to_cm360(sensitivity, find_game(game, games)["yaw"], dpi)


def sensitivity_for_cm360(cm360, game, dpi, games):
    """cm per 360 degrees at dpi (counts per inch) -> in-game sensitivity for game."""
    return cm360_to_sensitivity(cm360, find_game(game, games)["yaw"], dpi)


def convert_sensitivity(sensitivity, from_game, to_game, dpi, games):
    """Convert from_game sensitivity to to_game sensitivity at the same dpi, via cm/360."""
    if find_game(from_game, games) is find_game(to_game, games):
        return sensitivity
    cm360 = cm360_for_sensitivity(sensitivity, from_game, dpi, games)
    return sensitivity_for_cm360(cm360, to_game, dpi, games)


# This will only run when I run calculator.py directly
if __name__ == "__main__":

    c360 = sensitivity_to_cm360(1.0, 0.022, 1600)
    print(f"cm per 360: {c360:.2f}")

    sens = cm360_to_sensitivity(c360, 0.022, 1600)
    print(f"sensitivity: {sens:.2f}")
