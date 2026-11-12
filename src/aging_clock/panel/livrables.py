"""Programme « panel », livrables finaux : resultats_par_marqueur.csv et une fiche par marqueur.

Tout est tire des sorties publiques de Q1 a Q6 (reports/panel). Aucune valeur EFLM brute (option b).
"""
from __future__ import annotations

import ast
import json

import numpy as np
import pandas as pd

from .remesures import OUT

FICHES = OUT / "fiches"
# Q2, analyse secondaire 3 : effet du jeune non verifie sur la classification (points de personnes au-dessus du seuil, maximum)
Q2_CLASSE = {"glu_fast": "jusqu'à +31 points au seuil ADA (5,6 mmol/L) et +16 au seuil OMS si le jeûne n'est pas vérifié",
             "tg_fast": "jusqu'à +13 points au seuil de 1,7 mmol/L si le jeûne n'est pas vérifié",
             "homa_ir": "jusqu'à +39 points au-dessus d'un seuil illustratif si le jeûne n'est pas vérifié ; ne pas calculer sans jeûne vérifié",
             "quicki": "indice défini à jeun : ne pas calculer sans jeûne vérifié"}
GROUPES = {"tres_actifs": "très actifs", "pilule": "pilule", "injectable": "injectable", "menopause": "ménopause",
           "favorisee": "favorisée"}


def _num(x, d=1, sign=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace(".", ",").replace("-", "−")


def _g(x):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.3g}".replace(".", ",")


def _lit(s):
    return ast.literal_eval(s) if isinstance(s, str) and s.startswith("[") else None


def build() -> pd.DataFrame:
    q1 = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    a = q1[q1.groupe == "20-79 ans"].drop_duplicates("id").set_index("id")
    y = q1[q1.groupe == "30-55 ans"].drop_duplicates("id").set_index("id")
    iv = pd.read_csv(OUT / "Q1_interventions.csv")
    iv = iv[iv.groupe == "20-79 ans"]
    q2 = pd.read_csv(OUT / "Q2_synthese.csv").set_index("id")
    q3 = pd.read_csv(OUT / "Q3_synthese.csv")
    q4 = pd.read_csv(OUT / "Q4_synthese.csv")
    q5 = pd.read_csv(OUT / "Q5_synthese.csv").set_index("id")
    z6 = pd.read_csv(OUT / "Q6_zones.csv").set_index("id")
    c6 = pd.read_csv(OUT / "Q6_categories.csv")
    s6 = pd.read_csv(OUT / "Q6_sensibilites.csv")
    adj = pd.read_csv(OUT / "Q6_secondaire_ajustement_par_cote.csv")
    ra = pd.read_csv(OUT / "Q6_secondaire_risque_absolu.csv")
    q5k = pd.read_csv(OUT / "Q5_classification.csv").assign(a=lambda x: x.points.abs()).sort_values("a", ascending=False).drop_duplicates("id")
    ids = list(dict.fromkeys(list(a.index) + list(z6.index)))
    rows = []
    for mid in ids:
        r = {"id": mid, "marqueur": a.loc[mid, "marqueur"] if mid in a.index else mid}
        cov = []
        # ---- Q1
        if mid in a.index:
            cov.append("Q1")
            x = a.loc[mid]
            r |= {"echelle": x.echelle, "q1_jeu_principal": x.jeu_principal, "q1_cv_observe_pct": x.cv_obs_principal,
                  "q1_cv_6m_pct": x.cv_6m, "q1_statut": x.statut, "q1_cd6m_hausse_pct": x.cd6m_hausse, "q1_cd6m_baisse_pct": x.cd6m_baisse,
                  "q1_cd6m_unites": x.cd6m_unites, "q1_cd6m_hausse_robuste_pct": x.cd6m_hausse_robuste}
            if mid in y.index:
                r |= {"q1_cd6m_hausse_30_55_pct": y.loc[mid, "cd6m_hausse"], "q1_cd6m_baisse_30_55_pct": y.loc[mid, "cd6m_baisse"]}
            v = iv[iv.id == mid]
            if len(v):
                b = v.sort_values("ratio", ascending=False).iloc[0]
                r |= {"q1_n_interventions": len(v), "q1_intervention_max": b.intervention, "q1_effet_max_pct": b.effet_pct,
                      "q1_ratio_max": b.ratio, "q1_conclusion_max": b.conclusion, "q1_population_max": b.population}
        # ---- Q2
        if mid in q2.index:
            cov.append("Q2")
            x = q2.loc[mid]
            r |= {"q2_jeune_pct": x.jeune, "q2_ratio_jeune": x.ratio_jeune, "q2_heure_pct": x.heure, "q2_ratio_heure": x.ratio_heure,
                  "q2_categorie": x.categorie}
        if mid in Q2_CLASSE:
            r["q2_classement"] = Q2_CLASSE[mid]
        k5 = q5k[q5k.id == mid]
        if len(k5):
            w = k5.iloc[0]
            if abs(w.points) >= 5:
                r["q5_classement"] = f"{_num(w.points, 0, True)} points ({w.seuil}, événement {w.evenement})"
        # ---- Q3
        t = q3[(q3.id == mid) & q3.groupe.isin(GROUPES) & (q3.sexe.isin(["ensemble", "H", "F"]))]
        if len(t):
            cov.append("Q3")
            ina = t[t.categorie == "inadapté"]
            lab = []
            for _, w in ina.iterrows():
                if w.groupe == "menopause" and mid == "glu_fast":
                    continue  # requalifie (amendement du 2026-11-12) : risque reel, seuil a conserver
                lab.append(f"{GROUPES[w.groupe]}" + ("" if w.sexe == "ensemble" else f" ({w.sexe})"))
            r["q3_inadapte"] = "; ".join(dict.fromkeys(lab))
            if mid == "glu_fast":
                r["q3_note"] = "ménopause : risque réellement plus élevé, seuil à conserver (amendement du 2026-11-12)"
            d = t[t.categorie.isin(["décalé, sous le changement détectable", "inadapté"]) & t.rapport_au_cd.notna()]
            d = d[d.sexe == "ensemble"]
            if len(d):
                w = d.sort_values("rapport_au_cd", ascending=False).iloc[0]
                r |= {"q3_decalage_max_groupe": GROUPES[w.groupe], "q3_decalage_max": w.decalage, "q3_decalage_max_rapport_cd": w.rapport_au_cd}
        # ---- Q4
        t = q4[(q4.id == mid) & (q4.variante == "principal")]
        if len(t):
            cov.append("Q4")
            r["q4_normalisation"] = "; ".join(f"{w.type} {w.cote} : {w.conclusion}" for _, w in t.iterrows())
        # ---- Q5
        if mid in q5.index:
            cov.append("Q5")
            x = q5.loc[mid]
            r |= {"q5_ratio_max": x.ratio_max, "q5_evenement": x.evenement, "q5_categorie": x.categorie,
                  "q5_cd_deux_labos_hausse_pct": x.cd_deux_labos_hausse, "q5_ratio_entre_labos": x.ratio_entre_labos_c}
        # ---- Q6
        if mid in z6.index:
            cov.append("Q6")
            x = z6.loc[mid]
            r |= {"q6_forme_retenue": x.forme_retenue, "q6_minimum": x.xmin, "q6_minimum_sur_borne": x.min_sur_borne,
                  "q6_zone_risque_minimal": x.zone_min, "q6_seuil12_bas": x.seuil12_bas if x.cote_bas_retenu else np.nan,
                  "q6_seuil12_haut": x.seuil12_haut if x.cote_haut_retenu else np.nan,
                  "q6_seuil12_bas_valeur_retenue": x.seuil_bas_retenu, "q6_seuil12_haut_valeur_retenue": x.seuil_haut_retenu,
                  "q6_inter_sexe_repliquee": x.inter_sexe_repliquee,
                  "q6_inter_age_repliquee": bool((x.p_inter_age_dev < 0.05) and (x.p_inter_age_val or 1) < 0.05) if np.isfinite(x.p_inter_age_val or np.nan) else False}
            c = c6[c6.id == mid]
            r["q6_categories_d1"] = "; ".join(f"{w.type}{'' if w.sexe == 'H+F' else ' ' + w.sexe} {w.cote} : {w.categorie}" for _, w in c.iterrows())
            s1 = s6[(s6.id == mid) & s6.sensibilite.str.startswith("1")]
            ch = s1.changement_net.iloc[0] if len(s1) else None
            keep = []  # seuls les changements qui touchent un cote retenu en validation
            for part in (ch.split("; ") if isinstance(ch, str) and ch else []):
                side = "bas" if " bas" in part else "haut"
                if x[f"cote_{side}_retenu"] in (True, "True"):
                    keep.append(part)
            r["q6_marqueur_de_maladie"] = "; ".join(keep)
            j = adj[adj.id == mid]
            col = "classe_avec_alcool" if "classe_avec_alcool" in j else "classe"
            r["q6_ajustement"] = "; ".join(f"{w.cote} : {w[col]}" for _, w in j.iterrows())
            k = ra[(ra.id == mid) & (ra.niveau_hr == 1.2)]
            if len(k):
                r["q6_part_30_55_au_dela_seuil12"] = "; ".join(f"{w.cote} : {100 * w.part_30_55_ponderee:.0f} %" for _, w in k.iterrows())
                r["q6_ecart_risque_45ans_seuil12_points_H_F"] = f"{k.difference_points_H.median():.1f} / {k.difference_points_F.median():.1f}"
        r["couverture"] = " ".join(cov)
        rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ fiches
def _conclusion(r):
    lines = []
    # 1. suivre
    if pd.notna(r.get("q1_cd6m_hausse_pct")):
        s = f"Suivre : un changement n'est détectable chez une personne qu'à partir de {_num(r.q1_cd6m_hausse_pct, 0, True)} % / {_num(-abs(r.q1_cd6m_baisse_pct), 0, True)} % en 6 mois ({r.q1_statut})"
    elif pd.notna(r.get("q1_cd6m_unites")):
        s = f"Suivre : un changement n'est détectable qu'à partir de ± {_g(r.q1_cd6m_unites)} unités en 6 mois ({r.q1_statut})"
    else:
        s = "Suivre : changement détectable non estimable"
    if pd.notna(r.get("q1_ratio_max")):
        s += f" ; la meilleure intervention étudiée ({r.q1_intervention_max}) atteint {_num(r.q1_ratio_max, 2)} fois ce seuil : {r.q1_conclusion_max}."
    else:
        s += "."
    lines.append(s)
    # 2. pieges
    p = []
    if pd.notna(r.get("q5_categorie")) and r.q5_categorie not in ("négligeable au regard du bruit", "non estimable"):
        p.append(f"changement de méthode ou de laboratoire ({r.q5_categorie}, ratio {_num(r.q5_ratio_max, 2)})")
    if isinstance(r.get("q3_inadapte"), str) and r.q3_inadapte:
        p.append(f"seuils inadaptés pour : {r.q3_inadapte}")
    if pd.notna(r.get("q3_decalage_max_rapport_cd")) and r.q3_decalage_max_rapport_cd >= 0.5:
        p.append(f"décalage de {_num(r.q3_decalage_max, 0, True)} % chez les personnes « {r.q3_decalage_max_groupe} » ({_num(r.q3_decalage_max_rapport_cd, 2)} fois le changement détectable)")
    if isinstance(r.get("q2_classement"), str):
        p.append(f"pour classer, jeûne : {r.q2_classement}")
    if isinstance(r.get("q5_classement"), str):
        p.append(f"pour classer, changement de méthode : {r.q5_classement}")
    if pd.notna(r.get("q2_ratio_jeune")) and max(r.q2_ratio_jeune, r.get("q2_ratio_heure") or 0) >= 0.3:
        p.append(f"jeûne ou heure (ratios {_num(r.q2_ratio_jeune, 2)} et {_num(r.q2_ratio_heure, 2)})")
    if isinstance(r.get("q4_normalisation"), str) and "confirmer" in r.q4_normalisation:
        p.append("une anomalie limite se normalise souvent seule : confirmer avant de signaler")
    lines.append("Pièges : " + ("; ".join(p) if p else "aucun piège majeur repéré dans Q2 à Q5") + ".")
    # 3. risque
    if isinstance(r.get("q6_forme_retenue"), str):
        s = f"Risque (mortalité à 10 ans, association) : forme {r.q6_forme_retenue}"
        z = _lit(r.get("q6_zone_risque_minimal"))
        if z:
            s += f", zone de risque minimal {_g(z[0])}–{_g(z[1])}"
        th = [f"HR 1,2 sous {_g(r.q6_seuil12_bas)}" if pd.notna(r.get("q6_seuil12_bas")) else None,
              f"HR 1,2 au-dessus de {_g(r.q6_seuil12_haut)}" if pd.notna(r.get("q6_seuil12_haut")) else None]
        th = [x for x in th if x]
        if th:
            s += " ; " + " et ".join(th)
        if isinstance(r.get("q6_marqueur_de_maladie"), str) and r.q6_marqueur_de_maladie:
            s += f" ; marqueur de maladie probable ({r.q6_marqueur_de_maladie} sans les décès précoces)"
        lines.append(s + ".")
    else:
        lines.append("Risque : non étudié (moins de 1 000 décès ou absent de NHANES 1999-2010).")
    return lines


def fiche(r) -> str:
    L = [f"# {r.marqueur} (`{r.id}`)", "",
         "Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). "
         "Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).", "",
         "## Conclusion en trois lignes", ""]
    L += [f"{i}. {s}" for i, s in enumerate(_conclusion(r), 1)]
    L += ["", f"Couverture : {r.couverture}.", ""]
    if "Q1" in r.couverture:
        L += ["## Q1 : bruit de mesure et changement détectable", "",
              f"- CV observé : {_num(r.get('q1_cv_observe_pct'))} % (jeu {r.get('q1_jeu_principal')}) ; CV à 6 mois : {_num(r.get('q1_cv_6m_pct'))} %.",
              f"- Changement détectable à 6 mois, 20-79 ans : {_num(r.get('q1_cd6m_hausse_pct'), 0, True)} % / {_num(-abs(r.get('q1_cd6m_baisse_pct')), 0, True)} %"
              + (f" ; 30-55 ans : {_num(r.get('q1_cd6m_hausse_30_55_pct'), 0, True)} % / {_num(-abs(r.get('q1_cd6m_baisse_30_55_pct')), 0, True)} %" if pd.notna(r.get("q1_cd6m_hausse_30_55_pct")) else "")
              + (f" ; échelle additive : ± {_g(r.get('q1_cd6m_unites'))} unités" if pd.notna(r.get("q1_cd6m_unites")) else "") + ".",
              f"- Statut : {r.get('q1_statut')}."]
        if pd.notna(r.get("q1_ratio_max")):
            L.append(f"- Interventions étudiées : {int(r.q1_n_interventions)} ; la plus forte, {r.q1_intervention_max} ({r.q1_population_max}), "
                     f"{_num(r.q1_effet_max_pct, 1, True)} %, ratio {_num(r.q1_ratio_max, 2)} : {r.q1_conclusion_max}.")
        L.append("")
    if "Q2" in r.couverture:
        L += ["## Q2 : jeûne et heure", "",
              f"- Effet du jeûne (même personne) : {_num(r.q2_jeune_pct, 1, True)} % (ratio {_num(r.q2_ratio_jeune, 2)}) ; heure : "
              f"{_num(r.q2_heure_pct, 1, True)} % (ratio {_num(r.q2_ratio_heure, 2)}) ; catégorie : {r.q2_categorie}."]
        if isinstance(r.get("q2_classement"), str):
            L.append(f"- Pour classer : {r.q2_classement}.")
        L.append("")
    if "Q3" in r.couverture:
        L += ["## Q3 : populations particulières", "",
              f"- Seuils inadaptés : {r.get('q3_inadapte') or 'aucun groupe'}."]
        if isinstance(r.get("q3_note"), str):
            L.append(f"- Note : {r.q3_note}.")
        if pd.notna(r.get("q3_decalage_max")):
            L.append(f"- Plus grand décalage : {r.q3_decalage_max_groupe}, {_num(r.q3_decalage_max, 1, True)} % "
                     f"({_num(r.q3_decalage_max_rapport_cd, 2)} fois le changement détectable).")
        L.append("")
    if "Q4" in r.couverture:
        L += ["## Q4 : normalisation spontanée d'une anomalie", "", f"- {r.q4_normalisation}.", ""]
    if "Q5" in r.couverture:
        L += ["## Q5 : changements de méthode et de laboratoire", "",
              f"- Plus grand décalage de méthode NHANES : ratio {_num(r.get('q5_ratio_max'), 2)} (événement {r.get('q5_evenement') if pd.notna(r.get('q5_evenement')) else '—'}) ; "
              f"{r.get('q5_categorie')}."]
        if isinstance(r.get("q5_classement"), str):
            L.append(f"- Effet sur la classification : {r.q5_classement}.")
        if pd.notna(r.get("q5_cd_deux_labos_hausse_pct")):
            L.append(f"- Entre deux laboratoires de routine (littérature) : changement détectable {_num(r.q5_cd_deux_labos_hausse_pct, 0, True)} %.")
        L.append("")
    if "Q6" in r.couverture:
        L += ["## Q6 : zones fondées sur le risque de mortalité (association, pas cible)", "",
              f"- Forme retenue en validation : {r.q6_forme_retenue} ; minimum {_g(r.q6_minimum)}"
              + (" (sur une borne P5/P95)" if r.q6_minimum_sur_borne else "") + " ; zone de risque minimal "
              + "–".join(_g(v) for v in _lit(r.q6_zone_risque_minimal)) + ".",
              f"- Seuils HR 1,2 retenus : bas {_g(r.get('q6_seuil12_bas'))}, haut {_g(r.get('q6_seuil12_haut'))}.",
              f"- Comparaison aux bornes D1 : {r.get('q6_categories_d1') or '—'}."]
        if isinstance(r.get("q6_marqueur_de_maladie"), str) and r.q6_marqueur_de_maladie:
            L.append(f"- Sans les décès des 3 premières années : {r.q6_marqueur_de_maladie} (marqueur de maladie probable).")
        if isinstance(r.get("q6_ajustement"), str) and r.q6_ajustement:
            L.append(f"- Après ajustement (tabac, alcool, IMC, diabète, revenu) : {r.q6_ajustement}.")
        if isinstance(r.get("q6_part_30_55_au_dela_seuil12"), str):
            L.append(f"- 30-55 ans au-delà du seuil HR 1,2 : {r.q6_part_30_55_au_dela_seuil12} ; écart de risque de décès à 10 ans à 45 ans : "
                     f"+{r.q6_ecart_risque_45ans_seuil12_points_H_F.replace('.', ',').replace(' / ', ' / +')} point (hommes / femmes).")
        if r.get("q6_inter_sexe_repliquee") is True:
            L.append("- Interaction avec le sexe répliquée : lire les courbes par sexe.")
        if r.get("q6_inter_age_repliquee") is True:
            L.append("- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.")
        L += [f"- Figure : `../figures_q6/{r.id}.png`.", ""]
    return "\n".join(L)


def run():
    df = build()
    df.to_csv(OUT / "resultats_par_marqueur.csv", index=False)
    FICHES.mkdir(exist_ok=True)
    idx = ["# Fiches par marqueur", "", "| Marqueur | Couverture |", "|---|---|"]
    for _, r in df.iterrows():
        (FICHES / f"{r.id}.md").write_text(fiche(r), encoding="utf-8")
        idx.append(f"| [{r.marqueur}]({r.id}.md) | {r.couverture} |")
    (FICHES / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    return df


if __name__ == "__main__":
    run()
