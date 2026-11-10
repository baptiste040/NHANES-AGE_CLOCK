"""Points d'entree.

    python -m aging_clock score --input fichier.csv [--uncertainty]   # NumPy + pandas uniquement
    python -m aging_clock export                        # regenere le modele JSON
    python -m aging_clock validate --panel checkup_standard
    python -m aging_clock benchmark | equite
    python -m aging_clock fiabilite predictions | analyse

Les imports sont faits a la demande : la commande `score` ne charge ni lifelines ni le pipeline.
"""
import argparse


def main():
    parser = argparse.ArgumentParser(prog="aging_clock")
    sub = parser.add_subparsers(dest="command", required=True)

    s = sub.add_parser("score", help="calcule les ages biologiques d'un fichier CSV")
    s.add_argument("--input", required=True, help="CSV en unites canoniques (docs/specification_entrees.md)")
    s.add_argument("--output", default=None, help="CSV de sortie (defaut : <input>_scores.csv)")
    s.add_argument("--model", default=None, help="modele JSON (defaut : models/checkup_standard_v1.json)")
    s.add_argument("--uncertainty", action="store_true",
                   help="ajoute l'intervalle a 95 %% de chaque age biologique (Monte-Carlo)")
    s.add_argument("--variability", default=None, help="fichier des CV (defaut : config/variability.yaml)")
    s.add_argument("--draws", type=int, default=1000, help="nombre de remesures simulees")
    s.add_argument("--seed", type=int, default=2026)

    sub.add_parser("export", help="exporte le modele gele en JSON")
    v = sub.add_parser("validate", help="validation temporelle et rapport")
    v.add_argument("--panel", default="checkup_standard")
    v.add_argument("--bootstrap", type=int, default=None)
    b = sub.add_parser("benchmark", help="benchmark PhenoAge sur la validation")
    b.add_argument("--bootstrap", type=int, default=None)
    f = sub.add_parser("equite", help="audit d'equite sur la validation")
    f.add_argument("--bootstrap", type=int, default=None)
    sec = sub.add_parser("secondaire", help="validation secondaire 2015-2018")
    sec.add_argument("--bootstrap", type=int, default=None)
    sub.add_parser("incertitude", help="precision individuelle de l'age biologique (Monte-Carlo)")
    r = sub.add_parser("fiabilite", help="fiabilite test-retest sur les remesures NHANES 2001-2002")
    r.add_argument("etape", choices=["predictions", "analyse"])
    args = parser.parse_args()

    if args.command == "score":
        from . import score
        score.main(args.input, args.output, args.model, args.uncertainty, args.variability,
                   args.draws, args.seed)
    elif args.command == "export":
        from . import export
        print(f"Modele : {export.run()}")
    elif args.command == "validate":
        from . import report, validate
        out = validate.run(args.panel, n_boot=args.bootstrap)
        report.write(out)
        print(f"Rapport : {out / 'RESULTATS.md'}")
    elif args.command == "benchmark":
        from . import benchmark
        res = benchmark.run(n_boot=args.bootstrap)
        benchmark.write_report(res["dossier"])
        print(f"Benchmark : {res['dossier']}")
    elif args.command == "equite":
        from . import fairness
        res = fairness.run(n_boot=args.bootstrap)
        fairness.write_report(res["dossier"])
        print(f"Audit d'equite : {res['dossier']}")
    elif args.command == "incertitude":
        from . import uncertainty_report
        res = uncertainty_report.run()
        uncertainty_report.write_report(res["dossier"])
        print(f"Incertitude : {res['dossier']}")
    elif args.command == "fiabilite":
        from . import retest
        out = retest.predictions() if args.etape == "predictions" else retest.analyse()
        print(f"Fiabilite : {out}")
    elif args.command == "secondaire":
        from . import secondary
        res = secondary.run(n_boot=args.bootstrap)
        secondary.write_report(res["dossier"])
        print(f"Validation secondaire : {res['dossier']}")


if __name__ == "__main__":
    main()
