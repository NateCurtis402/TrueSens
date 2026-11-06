# Command-line interface for the sensitivity calculator, standard library only (argparse)
import argparse
import sys

from calculator import (
    cm360_for_sensitivity,
    convert_sensitivity,
    find_game,
    load_games,
    sensitivity_for_cm360,
)

REFERENCE_SENS = 1.0
REFERENCE_DPI = 1600


def build_parser():
    parser = argparse.ArgumentParser(
        description="Convert mouse sensitivity between games via cm/360.",
        epilog=(
            "examples:\n"
            "  python3 main.py --list\n"
            "  python3 main.py --dpi 1600 --sens 1.0 --from cs2 --to val\n"
            "  python3 main.py --dpi 1600 --sens 1.0 --from cs2\n"
            "  python3 main.py --dpi 1600 --cm360 30 --to ow2"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--list", action="store_true", help="list supported games and aliases")
    parser.add_argument("--dpi", type=float, help="mouse DPI (counts per inch)")
    value = parser.add_mutually_exclusive_group()
    value.add_argument("--sens", type=float, help="in-game sensitivity in the --from game")
    value.add_argument("--cm360", type=float, help="target cm per 360 degrees")
    parser.add_argument("--from", dest="from_game", metavar="GAME", help="game the --sens value is from")
    parser.add_argument("--to", dest="to_game", metavar="GAME", help="game to convert to")
    return parser


def validate(parser, args):
    """Reject missing or nonsensical argument combinations (argparse exits with status 2)."""
    if args.dpi is None:
        parser.error("--dpi is required")
    if args.sens is None and args.cm360 is None:
        parser.error("one of --sens or --cm360 is required")
    if args.sens is not None and args.from_game is None:
        parser.error("--sens requires --from")
    if args.cm360 is not None and args.to_game is None:
        parser.error("--cm360 requires --to")
    if args.cm360 is not None and args.from_game is not None:
        parser.error("--from cannot be used with --cm360")
    for flag, number in (("--dpi", args.dpi), ("--sens", args.sens), ("--cm360", args.cm360)):
        if number is not None and number <= 0:
            parser.error(f"{flag} must be greater than 0")


def print_list(games):
    for game in games:
        cm = cm360_for_sensitivity(REFERENCE_SENS, game["name"], REFERENCE_DPI, games)
        aliases = ", ".join(game.get("aliases", [])) or "none"
        print(
            f"{game['name']} — {cm:.1f} cm/360 for sens {REFERENCE_SENS:.1f} at {REFERENCE_DPI} DPI"
            f" (aliases: {aliases})"
        )


def run(args, games):
    if args.cm360 is not None:
        target = find_game(args.to_game, games)
        sens = sensitivity_for_cm360(args.cm360, target["name"], args.dpi, games)
        print(f"{target['name']}: {sens:.2f}")
        return

    source = find_game(args.from_game, games)
    if args.to_game is not None:
        target = find_game(args.to_game, games)
        sens = convert_sensitivity(args.sens, source["name"], target["name"], args.dpi, games)
        print(f"{target['name']}: {sens:.2f}")
        return

    cm = cm360_for_sensitivity(args.sens, source["name"], args.dpi, games)
    print(f"{source['name']} sens {args.sens:.2f} at {args.dpi:g} DPI = {cm:.1f} cm/360")
    print()
    width = max(len(game["name"]) for game in games)
    print(f"{'Game':<{width}}  Sensitivity")
    print(f"{'-' * width}  -----------")
    for game in games:
        sens = convert_sensitivity(args.sens, source["name"], game["name"], args.dpi, games)
        print(f"{game['name']:<{width}}  {sens:.2f}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    games = load_games()

    if args.list:
        print_list(games)
        return 0

    validate(parser, args)
    try:
        run(args, games)
    except KeyError as e:
        print(f"error: {e.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
