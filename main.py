import argparse
from src.logger import log
from src.orchestrator import Orchestrator


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Ativa logs de debug")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log.set_debug(args.debug)

    o = Orchestrator()
    if o.inicializa():
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
