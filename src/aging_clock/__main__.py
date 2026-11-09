"""Point d'entree : python -m aging_clock validate --panel checkup_standard"""
import argparse

from . import benchmark, report, validate


def main():
    parser = argparse.ArgumentParser(prog="aging_clock")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validation temporelle et rapport")
    v.add_argument("--panel", default="checkup_standard")
    v.add_argument("--bootstrap", type=int, default=None,
                   help="nombre de repliques (defaut : config/study.yaml)")
    b = sub.add_parser("benchmark", help="benchmark PhenoAge sur la validation")
    b.add_argument("--bootstrap", type=int, default=None)
    args = parser.parse_args()

    if args.command == "validate":
        out = validate.run(args.panel, n_boot=args.bootstrap)
        report.write(out)
        print(f"Rapport : {out / 'RESULTATS.md'}")
    elif args.command == "benchmark":
        res = benchmark.run(n_boot=args.bootstrap)
        benchmark.write_report(res["dossier"])
        print(f"Benchmark : {res['dossier']}")


if __name__ == "__main__":
    main()
