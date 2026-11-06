# TrueSens

TrueSens converts mouse sensitivity between competitive shooters using cm/360,
the physical distance your mouse travels for a full 360-degree in-game turn.
Give it your DPI and a sensitivity from one game (or a cm/360 target directly)
and it tells you the sensitivity that produces the same cm/360 in each other
supported game. It is a calculator: you type the result into the game yourself.

## The formula

Each game has a yaw value: degrees of camera rotation per mouse count at
sensitivity 1.0. From yaw, in-game sensitivity and DPI:

```
cm_per_360 = 360 / (yaw * sensitivity) / dpi * 2.54
```

The reverse (target cm/360 to in-game sensitivity) solves the same equation for
sensitivity. Reference value: CS2 (yaw 0.022) at sensitivity 1.0 and 1600 DPI is
25.977 cm/360.

## Supported games

| Game             | Yaw    | Aliases            |
|------------------|--------|--------------------|
| Valorant         | 0.07   | val, valo          |
| Counter-Strike 2 | 0.022  | cs2, csgo, cs      |
| Apex Legends     | 0.022  | apex               |
| Overwatch 2      | 0.0066 | ow2, overwatch, ow |
| Marvel Rivals    | 0.0175 | mr, rivals         |

All five yaw values come from a single cited source:
https://itsesports.com/tools/sensitivity-converter/

Caveat: yaw is a community-documented constant, not an official one. Riot has
never published Valorant's yaw, and published values for Marvel Rivals disagree
between sources (0.0175 vs 0.022). Verify against your own game before relying
on a result.

## Run it

Requires Python 3. The CLI and the calculator use only the standard library.

### CLI

```
python3 main.py --dpi 1600 --sens 1.0 --from cs2            # cm/360 plus a table for every game
python3 main.py --dpi 1600 --sens 1.0 --from cs2 --to val   # one game to another
python3 main.py --dpi 1600 --cm360 30 --to ow2              # cm/360 target to a game's sensitivity
python3 main.py --list                                      # supported games and aliases
```

Game names and aliases are case-insensitive.

### GUI

The GUI is built on PySide6, which is the only third-party dependency:

```
python3 -m venv .venv && .venv/bin/pip install PySide6 && .venv/bin/python gui.py
```

### Tests

```
python3 -m unittest discover -s tests -v
```

21 tests, standard library `unittest` only; pytest is not needed.

## How it works

- `calculator.py` - pure math and game lookup (`load_games`, `find_game`,
  conversion functions). No UI imports.
- `games.json` - game data: name, yaw, engine, source URL, aliases.
- `main.py` - command-line interface (argparse).
- `gui.py` - PySide6 front end; all math comes from `calculator.py`.
- `tests/` - unittest suites for the calculator and the CLI.

## Known limits

- No automatic game detection.
- Does not read or write any game config file.
- No installer or packaging yet; run from source.
- Competitive shooters only.

## Contributing

To add a game, add an entry to `games.json` with `name`, `yaw`, `engine`,
`source` (URL) and `aliases`. Every yaw value needs a cited source that
documents it; entries without one will not be accepted.
