"""Point d'entree : python -m aging_clock validate --panel checkup_standard"""
import argparse

from . import report, validate


def main():
    parser = argparse.ArgumentParser(prog="aging_clock")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validation temporelle et rapport")
    v.add_argument("--panel", default="checkup_standard")
    v.add_argument("--bootstrap", type=int, default=None,
                   help="nombre de repliques (defaut : config/study.yaml)")
    args = parser.parse_args()

    if args.command == "validate":
        out = validate.run(args.panel, n_boot=args.bootstrap)
        report.write(out)
        print(f"Rapport : {out / 'RESULTATS.md'}")


if __name__ == "__main__":
    main()
