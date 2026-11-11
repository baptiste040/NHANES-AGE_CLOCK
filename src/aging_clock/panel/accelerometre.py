"""Programme « panel », Q3 : resume de l'accelerometre NHANES 2003-2006 (PAXRAW), par personne.

Regles de Troiano et al. (Med Sci Sports Exerc 2008), utilisees par le NCHS :
- non-port : au moins 60 minutes consecutives a 0 coup, avec au plus 2 minutes consecutives entre
  1 et 100 coups ;
- jour valide : au moins 600 minutes de port ; personne retenue : au moins 4 jours valides ;
- activite moderee a vigoureuse (MVPA) chez l'adulte : minutes a 2 020 coups/minute ou plus ;
- donnees fiables seulement (PAXSTAT = 1, PAXCAL = 1).

Aucune valeur de marqueur n'est lue ici. Sortie : data/processed/panel/accelerometre_2003_2006.csv.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

from .remesures import ROOT

PAX = ROOT / "data" / "raw" / "panel" / "pax"
OUTF = ROOT / "data" / "processed" / "panel" / "accelerometre_2003_2006.csv"


def nonwear(c: np.ndarray) -> np.ndarray:
    """Masque de non-port pour une serie de minutes (coups)."""
    n = len(c)
    zero = c == 0
    low = (c >= 1) & (c <= 100)
    # suites de zeros
    edges = np.diff(np.concatenate([[0], zero.astype(int), [0]]))
    starts, ends = np.where(edges == 1)[0], np.where(edges == -1)[0]  # [start, end)
    mask = np.zeros(n, bool)
    if len(starts) == 0:
        return mask
    # fusion des suites separees par <= 2 minutes toutes entre 1 et 100 coups
    s0, e0 = starts[0], ends[0]
    spans = []
    for s, e in zip(starts[1:], ends[1:]):
        gap = s - e0
        if gap <= 2 and low[e0:s].all():
            e0 = e
        else:
            spans.append((s0, e0))
            s0, e0 = s, e
    spans.append((s0, e0))
    for s, e in spans:
        if e - s >= 60:
            mask[s:e] = True
    return mask


def _summarise(df: pd.DataFrame) -> list[dict]:
    rows = []
    for seqn, g in df.groupby("SEQN", sort=False):
        if not ((g.PAXSTAT == 1).all() and (g.PAXCAL == 1).all()):
            rows.append({"SEQN": int(seqn), "fiable": False})
            continue
        g = g.sort_values("PAXN")
        c = g.PAXINTEN.to_numpy(float)
        nw = nonwear(np.nan_to_num(c, nan=0))
        wear = ~nw
        day = g.PAXDAY.to_numpy()
        per = pd.DataFrame({"day": day, "wear": wear, "mvpa": wear & (c >= 2020), "vig": wear & (c >= 5999)})
        dd = per.groupby("day").sum()
        valid = dd[dd.wear >= 600]
        rows.append({"SEQN": int(seqn), "fiable": True, "jours_valides": int(len(valid)),
                     "mvpa_min_jour": float(valid.mvpa.mean()) if len(valid) else np.nan,
                     "vigoureux_min_jour": float(valid.vig.mean()) if len(valid) else np.nan,
                     "port_min_jour": float(valid.wear.mean()) if len(valid) else np.nan})
    return rows


def run(chunk=2_000_000) -> pd.DataFrame:
    out = []
    for cyc, z in ((2003, "PAXRAW_C.zip"), (2005, "PAXRAW_D.zip")):
        with zipfile.ZipFile(PAX / z) as zf:
            name = zf.namelist()[0]
            with zf.open(name) as fh:
                reader = pd.read_sas(io.BufferedReader(fh), format="xport", chunksize=chunk)
                carry = None
                for part in reader:
                    part = part[["SEQN", "PAXSTAT", "PAXCAL", "PAXDAY", "PAXN", "PAXINTEN"]]
                    if carry is not None:
                        part = pd.concat([carry, part])
                    last = part.SEQN.iloc[-1]
                    carry = part[part.SEQN == last]
                    done = part[part.SEQN != last]
                    for r in _summarise(done):
                        r["cycle"] = cyc
                        out.append(r)
                if carry is not None:
                    for r in _summarise(carry):
                        r["cycle"] = cyc
                        out.append(r)
        print(cyc, len(out), flush=True)
    res = pd.DataFrame(out)
    OUTF.parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(OUTF, index=False)
    return res


if __name__ == "__main__":
    run()
