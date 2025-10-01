import argparse
import subprocess
from neurocogdb.load.sync import sync_ddb
from neurocogdb.config.paths import config_root_path, confirm_root_path

def get_parser():
    parser = argparse.ArgumentParser(prog="neurocogdb")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # config
    config_parser = subparsers.add_parser("config", help="Set/View current configuration.")
    config_parser.add_argument(
        "--set",
        action="store_true",
        help="Set a new root path."
    )

    # sync
    subparsers.add_parser("sync", help="Sync catalog.")

    # gui
    subparsers.add_parser("gui", help="Launch catalog GUI.")

    return parser


def run_command(args):
    match args.command:
        case "config":
            if args.set:
                config_root_path()
                confirm_root_path()
            else:
                confirm_root_path()

        case "sync":
            sync_ddb()

        case "gui":
            subprocess.run(
                ["streamlit", "run", "neurocogdb/ddb/gui.py"],  # Command and its arguments as a list
                capture_output=True,
                text=True,  # Decodes stdout and stderr as text
                check=True,  # Raises CalledProcessError if the command returns a non-zero exit code
            )

        case _:
            raise ValueError(f"Unknown command: {args.command}")


def main():
    parser = get_parser()
    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
