#!/usr/bin/env python3
"""validate_discovery.py — Skill determinista del flujo 010_discovery (Tracer Bullet, L0).

Valida los 3 contratos fundacionales emitidos por el agente `foda-discovery` y verifica las
aserciones RED A1-A5 del cell_contract (A6 = determinismo, se prueba reejecutando; A7 = gate humano).

Reparto sintesis<->determinismo (design_system.md §6): la sintesis NL->estructura es del agente;
la validacion, el schema y la consistencia registro<->contrato son de esta skill (codigo).

Uso:
    python validate_discovery.py \
        --deliverables <dir con los 3 artefactos> \
        --schema <ruta a contract_data.schema.json> \
        --report <ruta de salida validation_report.json>

Salida: escribe validation_report.json (SIN timestamps -> determinismo A6). Exit 0 si ok, 1 si falla.
Dependencias: pyyaml, jsonschema (stdlib para el resto). Sin red.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: falta 'pyyaml' (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("ERROR: falta 'jsonschema' (pip install jsonschema)", file=sys.stderr)
    sys.exit(2)


REGISTER = "client_register.yaml"
HYPOTHESIS = "business_hypothesis.md"
CONTRACT = "contract_data.json"


def _load_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def validate(deliverables: Path, schema_path: Path) -> dict:
    """Corre A1-A5 y devuelve el reporte como dict (orden estable, sin timestamps)."""
    checks: list[dict] = []
    hallazgos: list[str] = []

    def record(check_id: str, ok: bool, detalle: str = "") -> bool:
        checks.append({"id": check_id, "ok": ok})
        if not ok and detalle:
            hallazgos.append(f"{check_id}: {detalle}")
        return ok

    reg_path = deliverables / REGISTER
    hyp_path = deliverables / HYPOTHESIS
    con_path = deliverables / CONTRACT

    # --- A1: existen y estan bien formados (YAML/JSON parseables, MD no vacio) ---
    register = None
    contract = None
    a1_ok = True

    reg_text = _load_text(reg_path)
    if reg_text is None:
        a1_ok = False
        hallazgos.append(f"A1: no se encuentra {REGISTER}")
    else:
        try:
            register = yaml.safe_load(reg_text)
            if not isinstance(register, dict):
                a1_ok = False
                hallazgos.append(f"A1: {REGISTER} no es un mapa YAML valido")
        except yaml.YAMLError as exc:
            a1_ok = False
            hallazgos.append(f"A1: {REGISTER} no parsea como YAML ({exc.__class__.__name__})")

    con_text = _load_text(con_path)
    if con_text is None:
        a1_ok = False
        hallazgos.append(f"A1: no se encuentra {CONTRACT}")
    else:
        try:
            contract = json.loads(con_text)
        except json.JSONDecodeError as exc:
            a1_ok = False
            hallazgos.append(f"A1: {CONTRACT} no parsea como JSON ({exc.msg})")

    hyp_text = _load_text(hyp_path)
    if hyp_text is None:
        a1_ok = False
        hallazgos.append(f"A1: no se encuentra {HYPOTHESIS}")
    elif not hyp_text.strip():
        a1_ok = False
        hallazgos.append(f"A1: {HYPOTHESIS} esta vacio")

    record("A1", a1_ok)

    # --- A2: contract_data.json valida contra su schema ---
    if contract is None:
        record("A2", False, "no hay contract_data.json parseable para validar")
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errores = sorted(
            Draft7Validator(schema).iter_errors(contract),
            key=lambda e: list(e.path),
        )
        if errores:
            # Mensaje estable: ruta + motivo, ordenado por path (determinismo).
            detalle = "; ".join(
                f"{'/'.join(str(p) for p in e.path) or '<raiz>'}: {e.message}"
                for e in errores
            )
            record("A2", False, detalle)
        else:
            record("A2", True)

    # --- A3: consistencia registro <-> contrato ---
    if register is None or contract is None:
        record("A3", False, "faltan registro y/o contrato para cotejar consistencia")
    else:
        problemas: list[str] = []

        # periodicidad
        if register.get("periodicidad") != contract.get("periodicidad"):
            problemas.append(
                f"periodicidad registro='{register.get('periodicidad')}' != "
                f"contrato='{contract.get('periodicidad')}'"
            )
        # horizonte_meses
        if register.get("horizonte_meses") != contract.get("horizonte_meses"):
            problemas.append(
                f"horizonte_meses registro='{register.get('horizonte_meses')}' != "
                f"contrato='{contract.get('horizonte_meses')}'"
            )
        # grain producto: cada nivel del contrato debe existir como clave del portafolio
        grain = contract.get("grain") or {}
        portafolio = register.get("portafolio") or {}
        for nivel in grain.get("producto", []):
            if nivel not in portafolio:
                problemas.append(f"nivel de grain producto '{nivel}' ausente en portafolio del registro")
        # grain geografia: cada nivel debe existir como clave de cobertura_geografica
        cobertura = register.get("cobertura_geografica") or {}
        for nivel in grain.get("geografia", []):
            if nivel not in cobertura:
                problemas.append(f"nivel de grain geografia '{nivel}' ausente en cobertura del registro")

        record("A3", not problemas, "; ".join(problemas))

    # --- A4: >=1 hipotesis con marca 'testeable_en:' ---
    if hyp_text is None:
        record("A4", False, "no hay business_hypothesis.md")
    else:
        n_test = len(re.findall(r"testeable_en\s*:", hyp_text))
        record("A4", n_test >= 1, f"hipotesis testeables encontradas={n_test} (se exige >=1)")

    # --- A5: >=3 areas entrevistadas distintas ---
    if register is None:
        record("A5", False, "no hay client_register.yaml")
    else:
        areas = register.get("areas_entrevistadas") or []
        distintas = sorted({str(a).strip().lower() for a in areas if str(a).strip()})
        record("A5", len(distintas) >= 3, f"areas distintas={len(distintas)} (se exigen >=3)")

    ok = all(c["ok"] for c in checks)
    return {"ok": ok, "checks": checks, "hallazgos": hallazgos}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida los 3 contratos de 010_discovery (L0).")
    parser.add_argument("--deliverables", required=True, type=Path,
                        help="Directorio con client_register.yaml, business_hypothesis.md, contract_data.json")
    parser.add_argument("--schema", required=True, type=Path,
                        help="Ruta a contract_data.schema.json")
    parser.add_argument("--report", required=True, type=Path,
                        help="Ruta de salida del validation_report.json")
    args = parser.parse_args(argv)

    report = validate(args.deliverables, args.schema)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    # Serializacion estable: indent fijo, sin sort (orden de construccion), newline final unico.
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"validation_report -> {args.report} (ok={report['ok']})")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
