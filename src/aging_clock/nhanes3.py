"""Lecture de NHANES III (1988-1994) : fichiers ASCII a positions fixes et programmes SAS du NCHS.

Seules les variables du panel sont lues. Codes « blanc mais applicable » / « ne sait pas »
(valeurs faites uniquement de 8 ou de 9 sur toute la largeur du champ, >= 3 chiffres) -> manquant.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ROOT

RAW = ROOT / "data" / "raw" / "nhanes3"
BASE = "https://wwwn.cdc.gov/nchs/data/nhanes3/"
FILES = {"lab": "1a/lab", "exam": "1a/exam", "labse": "3a/labse", "examse": "3a/examse"}
MORT = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/datalinkage/linked_mortality/NHANES_III_MORT_2019_PUBLIC.dat"


def layout(sas_path: Path) -> dict[str, tuple[int, int]]:
    """Positions (debut, fin) depuis le bloc INPUT d'un programme SAS du NCHS."""
    text = sas_path.read_text(encoding="latin1")
    block = text[text.upper().index("INPUT"):]
    block = block[:block.index(";")]
    pos = {}
    for name, a, b in re.findall(r"([A-Z][A-Z0-9_]*)\s+(\d+)(?:\s*-\s*(\d+))?", block):
        pos[name] = (int(a), int(b or a))
    return pos


# Resultats de laboratoire codes sur 2 chiffres ou « 88 » signifie « vide mais applicable » (correction
# du 2026-11-11, DECISIONS.md) : formule leucocytaire manuelle et bicarbonates. Ce code ne peut pas
# etre une vraie valeur (88 % de basophiles, 88 mmol/L de bicarbonates). Les autres champs a 2 chiffres
# (age, delai en jours) gardent 88 comme valeur reelle.
TWO_DIGIT_BLANK = {"MOPDIF", "EOP", "BOP", "C3PSI", "MORDIF", "EOR", "BOR", "C3RSI"}


def read_fixed(name: str, columns: list[str]) -> pd.DataFrame:
    """Lit les colonnes demandees du fichier `name` (lab, exam, labse, examse)."""
    pos = layout(RAW / f"{Path(FILES[name]).name}.sas")
    missing = [c for c in columns if c not in pos]
    if missing:
        raise KeyError(f"{name} : variables absentes {missing}")
    cols = ["SEQN"] + [c for c in columns if c != "SEQN"]
    specs = [(pos[c][0] - 1, pos[c][1]) for c in cols]
    df = pd.read_fwf(RAW / f"{Path(FILES[name]).name}.dat", colspecs=specs, names=cols,
                     dtype=str, header=None)
    out = pd.DataFrame({"SEQN": df["SEQN"].astype(int)})
    for c in cols[1:]:
        s = df[c].str.strip()
        width = pos[c][1] - pos[c][0] + 1
        code = s.str.fullmatch(r"8{3,}|9{3,}") & (s.str.len() == width)
        if c in TWO_DIGIT_BLANK:                       # champ a 2 chiffres : « 88 » = vide mais applicable
            code = code | s.str.fullmatch(r"88")
        v = pd.to_numeric(s, errors="coerce")
        out[c] = v.where(~code.fillna(False))
    return out.set_index("SEQN")


def seqn_only(name: str) -> set[int]:
    """Identifiants seulement (aucune autre colonne lue)."""
    pos = layout(RAW / f"{Path(FILES[name]).name}.sas")["SEQN"]
    s = pd.read_fwf(RAW / f"{Path(FILES[name]).name}.dat", colspecs=[(pos[0] - 1, pos[1])],
                    names=["SEQN"], header=None)["SEQN"]
    return set(s.astype(int))


def load_mortality() -> pd.DataFrame:
    from .nhanes import load_mortality as lm
    return lm(RAW / "NHANES_III_MORT_2019_PUBLIC.dat")
