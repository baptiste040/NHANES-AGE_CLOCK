"""Lecture et validation des fichiers de configuration YAML."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"

_ALLOWED_VAR_KEYS = {
    "unit", "system", "in_model", "range", "floor", "log", "spline", "alt_units",
}


@dataclass(frozen=True)
class Variable:
    name: str
    unit: str
    system: str
    in_model: bool = True
    range: tuple[float, float] | None = None
    floor: float | None = None
    log: bool = False
    spline: int | None = None
    alt_units: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Panel:
    name: str
    description: str
    version: int
    include_sex: bool
    systems: dict[str, str]
    variables: dict[str, Variable]
    sha256: str

    @property
    def model_variables(self) -> list[str]:
        return [v.name for v in self.variables.values() if v.in_model]

    def system_variables(self, system: str) -> list[str]:
        return [v.name for v in self.variables.values()
                if v.in_model and v.system == system]

    @property
    def active_systems(self) -> list[str]:
        return [s for s in self.systems if self.system_variables(s)]


def _read_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_study(path: Path | None = None) -> dict:
    return _read_yaml(path or CONFIG_DIR / "study.yaml")


def load_source(name: str = "nhanes") -> dict:
    return _read_yaml(CONFIG_DIR / "sources" / f"{name}.yaml")


def load_panel(name_or_path: str | Path) -> Panel:
    path = Path(name_or_path)
    if not path.suffix:
        path = CONFIG_DIR / "panels" / f"{name_or_path}.yaml"
    raw_bytes = path.read_bytes()
    raw = yaml.safe_load(raw_bytes)

    for key in ("name", "systems", "variables"):
        if key not in raw:
            raise ValueError(f"{path.name} : cle obligatoire manquante '{key}'")

    variables = {}
    for name, spec in raw["variables"].items():
        unknown = set(spec) - _ALLOWED_VAR_KEYS
        if unknown:
            raise ValueError(f"{name} : cles inconnues {sorted(unknown)}")
        if "unit" not in spec or "system" not in spec:
            raise ValueError(f"{name} : 'unit' et 'system' sont obligatoires")
        if spec["system"] not in raw["systems"]:
            raise ValueError(f"{name} : systeme inconnu '{spec['system']}'")
        rng = spec.get("range")
        if rng is not None and (len(rng) != 2 or rng[0] >= rng[1]):
            raise ValueError(f"{name} : plage invalide {rng}")
        spline = spec.get("spline")
        if spline is not None and spline < 3:
            raise ValueError(f"{name} : une spline demande au moins 3 noeuds")
        variables[name] = Variable(
            name=name,
            unit=spec["unit"],
            system=spec["system"],
            in_model=spec.get("in_model", True),
            range=tuple(rng) if rng is not None else None,
            floor=spec.get("floor"),
            log=spec.get("log", False),
            spline=spline,
            alt_units=spec.get("alt_units", {}),
        )

    return Panel(
        name=raw["name"],
        description=raw.get("description", ""),
        version=raw.get("version", 1),
        include_sex=raw.get("include_sex", True),
        systems=raw["systems"],
        variables=variables,
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
    )
