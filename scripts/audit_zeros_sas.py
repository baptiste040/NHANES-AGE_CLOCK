"""Audit du defaut de lecture des zeros (pandas read_sas, format xport) : les valeurs 0
sont rendues sous la forme d'un flottant minuscule (~5.4e-79).

Pour chaque fichier XPT de data/raw et chaque colonne lue par le pipeline, compte les valeurs
« zero minuscule » (0 < |x| < 1e-30) et les zeros exacts. Sortie : reports/audit_zeros_sas.csv.
Usage : python scripts/audit_zeros_sas.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TINY = 1e-30


def used_columns(src: dict) -> dict[str, set[str]]:
    """{fichier logique: colonnes NHANES lues}, tous cycles confondus."""
    used: dict[str, set[str]] = {}
    def add(f, v):
        if isinstance(v, dict):
            for x in v.values():
                add(f, x)
        elif isinstance(v, list):
            for x in v:
                add(f, x)
        elif v is not None:
            used.setdefault(f, set()).add(v)
    for block in ("demographics", "variables", "conditions"):
        for spec in src[block].values():
            add(spec["file"], spec["var"])
            if "ratio_to" in spec:
                add(spec["file"], spec["ratio_to"])
    for spec in src.get("treatments", {}).values():
        add(spec["file"], spec["chain"])
    add("RXQ", src["medications"]["use_var"])
    add("RXQ", "RXDDRGID")
    return used


def main() -> int:
    src = yaml.safe_load((ROOT / "config" / "sources" / "nhanes.yaml").read_text(encoding="utf-8"))
    used = used_columns(src)
    rows = []
    for year, files in src["cycles"].items():
        for logical, fname in files.items():
            path = RAW / f"{year}_{fname}.xpt"
            if not path.exists():
                rows.append({"cycle": year, "fichier": fname, "colonne": "(absent)"})
                continue
            df = pd.read_sas(path, format="xport", encoding="latin1")
            for col in df.columns:
                if not pd.api.types.is_float_dtype(df[col]):
                    continue
                x = df[col]
                tiny = int(((x != 0) & (x.abs() < TINY)).sum())
                if tiny or col in used.get(logical, set()):
                    rows.append({"cycle": year, "fichier": fname, "logique": logical, "colonne": col,
                                 "utilisee": col in used.get(logical, set()),
                                 "zeros_minuscules": tiny, "zeros_exacts": int((x == 0).sum()),
                                 "non_manquants": int(x.notna().sum())})
    # Fichiers lus hors config : medicaments, second examen 2001-2002, seances PH_B
    extra = ["RXQ_DRUG.xpt"] + [f"2001_{f}.xpt" for f in
                                ["L40_2_B", "L25_2_B", "L11_2_B", "L10_2_B", "L13_2_B", "L16_2_B", "PH_B"]]
    for name in extra:
        path = RAW / name
        if not path.exists():
            continue
        df = pd.read_sas(path, format="xport", encoding="latin1")
        for col in df.columns:
            if pd.api.types.is_float_dtype(df[col]):
                x = df[col]
                tiny = int(((x != 0) & (x.abs() < TINY)).sum())
                if tiny:
                    rows.append({"cycle": "-", "fichier": name, "logique": "hors config", "colonne": col,
                                 "utilisee": None, "zeros_minuscules": tiny,
                                 "zeros_exacts": int((x == 0).sum()), "non_manquants": int(x.notna().sum())})
    out = pd.DataFrame(rows)
    (ROOT / "reports").mkdir(exist_ok=True)
    out.to_csv(ROOT / "reports" / "audit_zeros_sas.csv", index=False)
    hit = out[(out["zeros_minuscules"].fillna(0) > 0)]
    print(hit[hit["utilisee"] != False].to_string(index=False))
    print(f"\nColonnes touchees (toutes) : {len(hit)} ; lues par le pipeline : {int((hit['utilisee'] == True).sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
