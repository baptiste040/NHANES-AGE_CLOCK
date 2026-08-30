"""src/load.py - Phase 1 : telechargement et chargement des donnees brutes."""
from pathlib import Path
import requests
import pandas as pd

DATA_DIR = Path("data/raw")

# Fichiers NHANES 2009-2010 (suffixe _F)
NHANES_FILES = {
    "DEMO":   "DEMO_F.xpt",     # demographie
    "BIOPRO": "BIOPRO_F.xpt",   # albumine, creat, glucose, PAL
    "CBC":    "CBC_F.xpt",      # lympho%, VGM, RDW, WBC
    "CRP":    "CRP_F.xpt",      # CRP standard (mg/dL)
}
NHANES_BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles"

MORT_FILE = "NHANES_2009_2010_MORT_2019_PUBLIC.dat"
MORT_URL = ("https://ftp.cdc.gov/pub/Health_Statistics/NCHS/"
            "datalinkage/linked_mortality/" + MORT_FILE)


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"[skip] deja present : {dest.name}")
        return dest
    print(f"[get ] {url}")
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"[ok  ] {dest.name} ({len(r.content)//1024} Ko)")
    return dest


def load_xpt(path):
    df = pd.read_sas(path, format="xport")
    df["SEQN"] = df["SEQN"].astype(int)
    return df


def load_mortality(path):
    colspecs = [(0, 6), (14, 15), (15, 16), (16, 19),
                (19, 20), (20, 21), (42, 45), (45, 48)]
    names = ["SEQN", "ELIGSTAT", "MORTSTAT", "UCOD_LEADING",
             "DIABETES", "HYPERTEN", "PERMTH_INT", "PERMTH_EXM"]
    df = pd.read_fwf(path, colspecs=colspecs, names=names, na_values=["", "."])
    df["SEQN"] = df["SEQN"].astype(int)
    return df


def main():
    frames = {}
    for key, fname in NHANES_FILES.items():
        p = download(f"{NHANES_BASE}/{fname}", DATA_DIR / fname)
        frames[key] = load_xpt(p)

    p = download(MORT_URL, DATA_DIR / MORT_FILE)
    frames["MORT"] = load_mortality(p)

    print("\n--- Milestone Phase 1 ---")
    for key, df in frames.items():
        print(f"{key:7s} -> {df.shape[0]:>6} lignes x {df.shape[1]:>2} col "
              f"| SEQN: {'SEQN' in df.columns}")
    return frames


if __name__ == "__main__":
    main()
