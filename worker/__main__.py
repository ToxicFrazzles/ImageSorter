import argparse
from pathlib import Path

from .worker import Worker
from . import config

parser = argparse.ArgumentParser(
    description="MediaManager auto-tagger worker."
)


def add_arguments():
    parser.add_argument(
        "--config", "-c",
        action="store",
        default=(Path(__file__).parent.parent / "worker_config.ini")
    )


def main():
    add_arguments()
    args = parser.parse_args()
    config.config = config.Config(Path(args.config).resolve())
    Worker().run()


if __name__ == "__main__":
    main()
