"""Programme « panel », Q3 : regeneration des tableaux du rapport depuis les CSV (ajout du 2026-11-12).

Avant les corrections d'erreurs du 2026-11-12, ces tableaux etaient recopies a la main. Les lignes
montrees suivent la regle du rapport (rapport au CD >= 0,3, ou « inadapte »), plus les marqueurs que
le rapport montrait deja (hemoglobine, creatinine, DFGe, etc.).
"""
from __future__ import annotations

import ast
import re

import numpy as np
import pandas as pd

from .remesures import DERIVED, LABEL, OUT

LAB = LABEL | {d[0]: d[1] for d in DERIVED} | {"acr": "Rapport albumine/créatinine urinaire", "ck": "CK", "tibc": "CTF",
                                               "vitd": "Vitamine D"}
INV = {"LDL": "ldl", "Vitamine D": "vitd", "CTF": "tibc"}
for k, v in LAB.items():
    INV.setdefault(v, k)


def _n(x, d=1, sign=True):
    if x is None or not np.isfinite(x):
        return "—"
    return (f"{x:+.{d}f}" if sign else f"{x:.{d}f}").replace(".", ",").replace("-", "−")


def _ci(c):
    c = ast.literal_eval(c) if isinstance(c, str) else c
    if not isinstance(c, (list, tuple)) or not np.all(np.isfinite(c)):
        return ""
    return f" [{_n(c[0])} ; {_n(c[1])}]"


def _load():
    sy = pd.read_csv(OUT / "Q3_synthese.csv")
    sh = pd.read_csv(OUT / "Q3_decalages.csv")
    m = sy.merge(sh[["groupe", "sexe", "id", "n_groupe", "decalage_moindres_carres", "echelle"]
                    + (["estimateur"] if "estimateur" in sh else [])], on=["groupe", "sexe", "id"], how="left")
    return m


def _pct(r):
    return "%" if r.echelle == "log" else ""


def _cat(r, old_cat=None):
    if old_cat and "risque réellement" in old_cat:
        return old_cat
    c = r.categorie
    if c == "inadapté":
        rt = r.regle_taux if isinstance(r.regle_taux, str) else ""
        rt = re.sub(r"\b(H|F|ensemble) ", "", rt).replace("(S)", "S").replace("(R)", "R")
        return "**inadapté**" + (f" (taux : {rt})" if rt else "")
    return c


def _row(r, label, old_cat=None):
    est = ("*" if isinstance(r.get("estimateur"), str) and r.estimateur.startswith("moindres") else "")
    return (f"| {label} | {int(r.n_groupe) if np.isfinite(r.n_groupe) else '—'} | {_n(r.decalage)} {_pct(r)}{_ci(r.ic95)}{est} | "
            f"{_n(r.decalage_moindres_carres)} | {_n(r.cd6m, 1, False)} | {_n(r.rapport_au_cd, 2, False)} | {_cat(r, old_cat)} |")


def regen_section_table(md: str, title_prefix: str, groupe: str, sexe: str, m: pd.DataFrame, exclude=()) -> str:
    i = md.index(title_prefix)
    h = md.index("| Marqueur | n groupe |", i)
    j = md.index("\n\n", h)
    old = md[h:j].split("\n")[2:]
    old_rows = {}
    for line in old:
        cells = [c.strip() for c in line.strip("|").split("|")]
        lab = cells[0]
        base = re.sub(r" \(.*\)$", "", lab) if lab not in INV else lab
        mid = INV.get(lab, INV.get(base))
        if mid:
            old_rows[mid] = (lab, cells[-1])
    g = m[(m.groupe == groupe) & (m.sexe == sexe)].copy()
    show = g[((g.rapport_au_cd >= 0.3) | (g.categorie == "inadapté") | g.id.isin(old_rows)) & (~g.id.isin(exclude) | g.id.isin(old_rows))]
    show = show.assign(_k=np.where(show.rapport_au_cd >= 0.3, 0, np.where(show.categorie == "inadapté", 1, 2)))
    show = show.sort_values(["_k", "rapport_au_cd"], ascending=[True, False])
    lines = md[h:j].split("\n")[:2]
    for _, r in show.iterrows():
        lab, oc = old_rows.get(r.id, (LAB.get(r.id, r.id), None))
        lines.append(_row(r, lab, oc))
    return md[:h] + "\n".join(lines) + md[j:]


def regen_compare_table(md: str, header: str, cols: list[tuple[str, str]], m: pd.DataFrame) -> str:
    """Tableau a colonnes = groupes (sexe « ensemble ») ; lignes = marqueurs deja presents."""
    h = md.index(header)
    j = md.index("\n\n", h)
    block = md[h:j].split("\n")
    out = block[:2]
    for line in block[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        lab = cells[0]
        mid = INV.get(lab) or INV.get(re.sub(r" \(.*\)$", "", lab))
        vals = []
        for (g, _), old in zip(cols, cells[1:]):
            x = m[(m.groupe == g) & (m.sexe == "ensemble") & (m.id == mid)] if mid else m.iloc[0:0]
            if not len(x) or not np.isfinite(x.decalage.iloc[0]):
                vals.append(old if "non estimable" in old else "non estimable")
                continue
            r = x.iloc[0]
            est = "*" if isinstance(r.get("estimateur"), str) and r.estimateur.startswith("moindres") else ""
            vals.append(f"{_n(r.decalage)} {_pct(r)}{_ci(r.ic95)}{est}")
        out.append("| " + " | ".join([lab] + vals) + " |")
    return md[:h] + "\n".join(out) + md[j:]


def run(path=OUT / "Q3_POPULATIONS.md"):
    md = path.read_text(encoding="utf-8")
    m = _load()
    for title, g, s, ex in [("### Très actifs, hommes", "tres_actifs", "H", ()), ("### Très actifs, femmes", "tres_actifs", "F", ()),
                            ("### Après la ménopause", "menopause", "ensemble", ()),
                            ("### Population favorisée", "favorisee", "ensemble", ("aip", "quicki", "globulin"))]:
        md = regen_section_table(md, title, g, s, m, ex)
    md = regen_compare_table(md, "| Marqueur | Principal (5 % par sexe, deux sexes ajustés) |",
                             [("tres_actifs", ""), ("tres_actifs_seuil_global", ""), ("tres_actifs_questionnaire", "")], m)
    md = regen_compare_table(md, "| Marqueur | Pilule (546) |",
                             [("pilule", ""), ("pilule_oestroprogestative", ""), ("injectable", "")], m)
    path.write_text(md, encoding="utf-8", newline="")
    return md


if __name__ == "__main__":
    run()
