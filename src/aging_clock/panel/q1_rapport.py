"""Programme « panel », Q1 : tableaux du rapport, generes depuis les CSV (ajout du 2026-11-12).

Avant les corrections d'erreurs du 2026-11-12, ces tableaux etaient recopies a la main.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .remesures import OUT

JEU = {"nhanes3": "NHANES III", "2001_2002": "2001-02"}


def _n(x, d=0, sign=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace(".", ",").replace("-", "−")


def _cd(h, b):
    if pd.isna(h):
        return "—"
    return f"+{_n(h)} / −{_n(abs(b))}"


def _src(s):
    return str(s).split(", ")[0]


def table_cd() -> str:
    t = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    a = t[(t.groupe == "20-79 ans") & ~t.statut.astype(str).str.startswith("EFLM")]
    y = t[t.groupe == "30-55 ans"].drop_duplicates("id").set_index("id")
    lines = ["| Marqueur | Jeu principal | n | CV observé (%) | **Changement détectable à 6 mois (%)**, hausse / baisse, 20-79 ans "
             "| 30-55 ans | Avec le bruit de NHANES III (sensibilité) | Statut |", "|---|---|---|---|---|---|---|---|"]
    for _, r in a.iterrows():
        jeu = r.jeu_principal if isinstance(r.jeu_principal, str) else None
        if jeu is None:
            lines.append(f"| {r.marqueur} | — | — | — | — | — | — | {r.statut} |")
            continue
        n = int(r[f"n_{jeu}"])
        z = y.loc[r.id] if r.id in y.index else None
        if r.echelle == "log":
            cv = _n(r.cv_obs_principal, 1)
            main = f"**{_cd(r.cd6m_hausse, r.cd6m_baisse)}**"
            sub = _cd(z.cd6m_hausse, z.cd6m_baisse) if z is not None else "—"
            nh3 = _cd(r.get("cd6m_hausse_nhanes3"), r.get("cd6m_baisse_nhanes3")) if jeu == "2001_2002" else "(jeu principal)"
        else:
            cv = f"ET intra {_n(r.sd_intra_principal, 2)}"
            main = f"**± {_n(r.cd6m_unites, 2)} (unités)**"
            sub = f"± {_n(z.cd6m_unites, 2)}" if z is not None and pd.notna(z.get("cd6m_unites")) else "—"
            nh3 = "—"
        lines.append(f"| {r.marqueur} | {JEU[jeu]} | {n} | {cv} | {main} | {sub} | {nh3} | {r.statut} |")
    return "\n".join(lines)


def _concl_short(c):
    return c


def table_interventions() -> str:
    t = pd.read_csv(OUT / "Q1_interventions.csv")
    a = t[t.groupe == "20-79 ans"].reset_index(drop=True)
    b = t[t.groupe == "30-55 ans"].set_index(["intervention", "id"])
    lines = ["| Intervention | Marqueur | Effet moyen | Changement détectable à 6 mois | **Ratio**, 20-79 ans | Ratio, 30-55 ans "
             "| Ratio avec le bruit de NHANES III | Conclusion | Source (lecture) ; population |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in a.iterrows():
        rb = b.loc[(r.intervention, r.id)] if (r.intervention, r.id) in b.index else None
        lines.append(f"| {r.intervention} | {r.marqueur} | {_n(r.effet_pct, 0, True)} % | {_n(r.cd6m_pct)} % | **{_n(r.ratio, 2)}** | "
                     f"{_n(rb.ratio, 2) if rb is not None else '—'} | {_n(r.ratio_cd_nhanes3, 2)} | {r.conclusion} | "
                     f"{_src(r.source)} ({r.lu}) ; {r.population} |")
    return "\n".join(lines)


def _k(x):
    if isinstance(x, str) and not x.replace(".", "").isdigit():
        return x
    v = int(float(x))
    return "> 100" if v > 100 else str(v)


def table_moyenner() -> str:
    t = pd.read_csv(OUT / "Q1_secondaire_moyenner.csv")
    a = t[t.groupe == "20-79 ans"].reset_index(drop=True)
    b = t[t.groupe == "30-55 ans"].set_index(["intervention", "id"])
    lines = ["| Intervention | Marqueur | Population | Effet moyen | Ratio | **A : prises de sang par bilan** | **B : bilans avant et après** "
             "| 30-55 ans (A / B) | Source (lecture) |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in a.iterrows():
        rb = b.loc[(r.intervention, r.id)] if (r.intervention, r.id) in b.index else None
        if isinstance(rb, pd.DataFrame):
            rb = rb.iloc[0]
        sub = f"{_k(rb.prelevements_par_bilan_k)} / {_k(rb.bilans_avant_et_apres_m)}" if rb is not None else "—"
        lines.append(f"| {r.intervention} | {r.marqueur} | {r.population} | {_n(r.effet_pct, 0, True)} % | {_n(r.ratio, 2)} | "
                     f"**{_k(r.prelevements_par_bilan_k)}** | **{_k(r.bilans_avant_et_apres_m)}** | {sub} | {_src(r.source)} ({r.lu}) |")
    return "\n".join(lines)


def table_rcv() -> str:
    t = pd.read_csv(OUT / "Q1_comparaison_rcv_publies.csv")
    lines = ["| Marqueur | Avant (NHANES III) | **Après (2001-2002)** | RCV Westgard 2014 | Rapport Westgard avant → **après** (hausse) "
             "| Rapport Westgard après (baisse) | RCV EFLM | Rapport EFLM après (hausse / baisse) |", "|---|---|---|---|---|---|---|---|"]
    for _, r in t.iterrows():
        lines.append(f"| {r.marqueur} | +{r.cd6m_hausse_avant} / −{r.cd6m_baisse_avant} | **{_cd(r.cd6m_hausse, r.cd6m_baisse)}** | "
                     f"+{r.rcv_westgard_hausse} / −{r.rcv_westgard_baisse} | {_n(r.rapport_westgard_hausse_avant, 2)} → **{_n(r.rapport_westgard_hausse, 2)}** | "
                     f"{_n(r.rapport_westgard_baisse, 2)} | +{r.rcv_eflm_hausse} / −{r.rcv_eflm_baisse} | "
                     f"{_n(r.rapport_eflm_hausse, 2)} / {_n(r.rapport_eflm_baisse, 2)} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(table_rcv())
