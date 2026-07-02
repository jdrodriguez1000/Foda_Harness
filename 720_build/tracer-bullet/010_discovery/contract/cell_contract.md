# Cell contract — `010_discovery` × Tracer Bullet (L0)

> **Paso:** Ejecutar → artefacto #1 de 4 (`710_plan/tracer-bullet/010_discovery.md §1`).
> **Qué es:** la **fuente de verdad de "terminado"** de esta celda. El paso *Probar* verifica las
> aserciones RED con la skill `validate_discovery.py`; el paso *Verificar* audita contra este contrato,
> `slice_contract §2 fila 010` y el brief L0.
> **Banda:** `tracer-bullet` · **Flujo:** `010_discovery` · **Peldaño:** `L0` · **Capa:** `—` (pre-ingestión).
> **Estado:** `PROPUESTO` · **Fecha:** `2026-07-01`.

---

## 1. Frontera de la celda (I/O)

| | Nombre | Forma | Ruta |
|---|--------|-------|------|
| **Entrada** | `business_questionnaire_answered.md` | Markdown NL | `720_build/golden_client/C1/questionnaires/` |
| **Entrada** | `systems_questionnaire_answered.md` | Markdown NL | idem |
| **Salida** | `client_register.yaml` | YAML | `720_build/tracer-bullet/010_discovery/deliverables/` |
| **Salida** | `business_hypothesis.md` | Markdown | `…/deliverables/` |
| **Salida** | `contract_data.json` | JSON (schema-validado) | `…/deliverables/` |
| **Reporte** | `validation_report.json` | JSON (sin timestamp) | `…/evaluation/` |

> **Planos (`D-001`):** en la instancia real los 3 artefactos son runtime `fda-*` (carpeta del cliente).
> Aquí se emiten a `deliverables/` **solo para construir y probar** la celda contra el golden client C1
> (`D-012`). No tocan bronze/silver/gold.

## 2. Done L0 (acotado del brief §6)

La celda está **terminada** cuando:

1. Existen los **3 contratos fundacionales** bien formados (YAML/JSON parseables, MD no vacío) y
   **mutuamente consistentes** (lo declarado en `client_register.yaml` coincide con `contract_data.json`).
2. `contract_data.json` declara de forma **inequívoca**: archivos esperados, medio de acceso (`csv`),
   **periodicidad** (`mensual`), horizonte (`6` meses) y el **grain** producto × geografía (`D-014`).
3. `business_hypothesis.md` contiene **≥1 hipótesis** formulada de forma **testeable**
   (verificable aguas abajo en `040_exploration`).
4. La **cobertura de áreas** queda reflejada: `areas_entrevistadas` con **≥3 áreas distintas**
   (p. ej. Planeación, Comercial, Logística).
5. La skill `validate_discovery.py` emite `validation_report.json` con `ok: true` y es **determinista**
   (mismo input ⇒ mismo reporte, sin timestamps).
6. **Gate humano (obligatorio):** el científico de datos **aprueba explícitamente** los 3 artefactos
   antes de habilitar `015_onboarding` (`CLAUDE.md §5`).

> **Fuera de L0 (difiere a L1+, no se exige aquí):** intake en vivo multi-stakeholder ·
> `problem_statement.md` (L1) / `data_structure.md` (L2) · cuestionario dinámico y detección de
> contradicciones (L3) · grain multinivel exhaustivo · modo Ajuste · evaluador C calibrado (TR-3).

## 3. Aserciones RED (checklist verificable — diseño §5)

> Las #1–#6 las verifica la skill de forma determinista; la #7 es inspección humana (gate).

| # | Aserción | Verifica |
|---|----------|----------|
| **A1** | Existen los 3 artefactos y están bien formados (YAML/JSON parseables, MD no vacío). | skill |
| **A2** | `contract_data.json` **valida contra su schema** y declara inequívoco grain + periodicidad + medio + archivos + horizonte. | skill (`jsonschema`) |
| **A3** | **Consistencia registro ⇄ contrato:** periodicidad, niveles de grain y sede/nº SKUs coinciden entre `client_register.yaml` y `contract_data.json`. | skill |
| **A4** | `business_hypothesis.md` tiene **≥1** hipótesis con marca `testeable_en:`. | skill (regex) |
| **A5** | `areas_entrevistadas` refleja **≥3 áreas distintas**. | skill |
| **A6** | **Determinismo:** validar dos veces el mismo input produce un `validation_report.json` idéntico (byte a byte). | skill (reejecución) |
| **A7** | **Gate humano:** el DS aprueba explícitamente antes de habilitar `015_onboarding`. | humano |

## 4. Formato esperado del `validation_report.json`

```json
{
  "ok": true,
  "checks": [
    { "id": "A1", "ok": true },
    { "id": "A2", "ok": true },
    { "id": "A3", "ok": true },
    { "id": "A4", "ok": true },
    { "id": "A5", "ok": true }
  ],
  "hallazgos": []
}
```

> Sin campo de tiempo ni ruta absoluta variable → garantiza el determinismo de **A6**.
> `ok` es `true` sólo si **todas** las checks A1–A5 pasan. Exit code `0` si `ok`, `1` si falla.

## 5. Trazabilidad

- **Brief:** `700_brief/010_discovery.md §6` (Done) y §9 (escalera, fila L0).
- **Banda:** `703_definition/tracer-bullet/slice_contract.md §2` (fila 010) y `bdd.md`.
- **Diseño:** `705_design/tracer-bullet/010_discovery.md` (§5 aserciones, APROBADO).
- **Plan:** `710_plan/tracer-bullet/010_discovery.md` (orden de construcción).
