"""Lecture des fichiers ASCII a positions fixes de NHANES III."""
import numpy as np

from aging_clock import nhanes3


def test_layout_and_missing_codes(tmp_path, monkeypatch):
    (tmp_path / "lab.sas").write_text(
        "DATA X;\n INPUT\n   SEQN 1-5\n   AMPSI 6-8\n   CRP 9-13\n   HSSEX 14\n;\nRUN;\n", encoding="latin1")
    (tmp_path / "lab.dat").write_text("00001 42 0.21 1\n00002888888882\n00003 3925.201\n", encoding="latin1")
    monkeypatch.setattr(nhanes3, "RAW", tmp_path)
    assert nhanes3.layout(tmp_path / "lab.sas")["CRP"] == (9, 13)
    d = nhanes3.read_fixed("lab", ["AMPSI", "CRP", "HSSEX"])
    assert d.loc[1, "AMPSI"] == 42 and d.loc[1, "CRP"] == 0.21
    assert np.isnan(d.loc[2, "AMPSI"]) and np.isnan(d.loc[2, "CRP"])      # 888 / 88888 -> manquant
    assert d.loc[3, "CRP"] == 25.20 and d.loc[3, "HSSEX"] == 1
    assert nhanes3.seqn_only("lab") == {1, 2, 3}
