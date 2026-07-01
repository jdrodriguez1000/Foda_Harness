# Diseño de celda — `010_discovery` × Tracer Bullet (L0)

> **Paso:** Diseñar (`D-029`, `methodology.md §7`). Peso **ligero** (E4): el alcance vive en el
> `slice_contract` de la banda. **Un archivo por celda.**
> **Banda:** `tracer-bullet` · **Flujo:** `010_discovery` · **Peldaño:** `L0` · **Capa:** `—` (pre-ingestión).
> **Insumos del diseño:** `700_brief/010_discovery.md` (escalera L0→Ln) · `703_definition/tracer-bullet/{slice_contract.md,bdd.md}` (§2 fila 010) · `700_brief/000_general_process.md` (I/O) · `955_architecture/design_system.md` (stack `D-023..D-027`).
> **Estado:** `PROPUESTO` · **Fecha:** `2026-07-01`.

---

## 1. Qué construye esta celda (una frase)

A partir de **dos cuestionarios ya respondidos** de C1 (negocio + sistemas), un agente sintetiza los
**3 contratos fundacionales** en su forma mínima y los valida con **código determinista**; gate humano
simple (aprobar/rechazar). **No** hay intake en vivo, ni documentos legibles ricos, ni modo Ajuste (L1+).

## 2. Contrato I/O de la celda (frontera)

| | Nombre | Forma | Origen / Destino |
|---|--------|-------|------------------|
| **Entrada** | `business_questionnaire_answered.md` | Markdown NL | `720_build/golden_client/C1/questionnaires/` |
| **Entrada** | `systems_questionnaire_answered.md` | Markdown NL | idem |
| **Salida** | `client_register.yaml` | YAML | `deliverables/` |
| **Salida** | `business_hypothesis.md` | Markdown | `deliverables/` |
| **Salida** | `contract_data.json` | JSON (schema-validado) | `deliverables/` |

> En la instancia real estos 3 artefactos son runtime `fda-*` (carpeta del cliente). Para **construir/probar**
> la celda se emiten a `deliverables/` contra el golden client C1 (`D-012`). No tocan bronze/silver/gold.

## 3. Componentes de la celda (`720_build/tracer-bullet/010_discovery/`)

- **`agents/foda-discovery.md`** — worker del flujo (síntesis LLM). Lee los 2 cuestionarios y **redacta**
  los 3 artefactos. `tools: Read, Write` (+ invoca la skill). Sin `Agent` (modelo plano `D-009`).
  Reparto síntesis↔determinismo (`design_system.md §6`): la **síntesis NL→estructura** es del agente; la
  **validación y consistencia** es de la skill.
- **`skills/validate_discovery.py`** — código determinista (Python, stdlib + `pyyaml`). Valida:
  (a) `contract_data.json` contra su JSON Schema; (b) `client_register.yaml` bien formado;
  (c) **consistencia registro ⇄ contrato** (grain, periodicidad, sede/SKUs coinciden); (d) `business_hypothesis.md`
  tiene ≥1 hipótesis con marca testeable. Salida: `evaluation/validation_report.json` (`ok|fail` + hallazgos).
- **`schemas/contract_data.schema.json`** — JSON Schema del contrato de datos (campos obligatorios: `archivos_esperados`,
  `medio_acceso`, `periodicidad`, `grain.producto[]`, `grain.geografia[]`, `financieros_en_fuente[]`).
- **`contract/cell_contract.md`** — Done de la celda + aserciones RED (checklist que la skill verifica).

## 4. Estructura mínima de cada artefacto (L0)

- **`client_register.yaml`:** `razon_social`, `sector`, `cobertura_geografica`, `portafolio` (familia/categoría/
  subcategoría/nº SKUs), `problema` (1 frase), `horizonte_meses`, `periodicidad`, `areas_entrevistadas[]` (≥3).
- **`business_hypothesis.md`:** ≥1 hipótesis **testeable** (formato `H1: … | testeable_en: 040_exploration`).
  De C1 salen 3 naturales (estacionalidad dic., heterogeneidad SKU, precio↓⇒demanda↑) → basta declarar ≥1.
- **`contract_data.json`:** `{archivos_esperados, medio_acceso:"csv", periodicidad:"mensual", horizonte_meses:6,
  grain:{producto:[familia,categoria,subcategoria,sku], geografia:[region,pais,ciudad,sede]},
  financieros_en_fuente:[precio_unitario_venta,costo_unitario_venta,costo_inventario]}`.

## 5. Aserciones de aceptación (semillas del paso RED / Probar)

1. Existen los 3 artefactos, bien formados (YAML/JSON parseables, MD no vacío).
2. `contract_data.json` valida contra su schema y declara **inequívoco** grain + periodicidad + medio + archivos.
3. **Consistencia registro ⇄ contrato:** periodicidad, grain y sede/SKUs coinciden entre ambos.
4. `business_hypothesis.md` tiene **≥1** hipótesis con marca `testeable_en`.
5. `areas_entrevistadas` refleja **≥3 áreas distintas** (Planeación, Comercial, Logística).
6. **Determinismo de la skill:** validar dos veces el mismo input da el mismo `validation_report.json`.
7. **Gate humano:** el DS aprueba explícitamente antes de habilitar `015_onboarding`.

## 6. Fuera de alcance (difiere a L1+, no diseñar aquí)

Intake en vivo multi-stakeholder · `problem_statement.md` (L1) / `data_structure.md` (L2) · cuestionario
dinámico y detección de contradicciones (L3) · grain multinivel exhaustivo · modo Ajuste · evaluador C
calibrado (TR-3) · durabilidad/checkpoints (TR-4).

## 7. Riesgos de esta celda

- **Grain mal declarado** envenena aguas abajo (`D-014`): mitiga la aserción #3 (consistencia registro⇄contrato).
- **Confusión de planos:** los 3 artefactos son `fda-*`; en construcción viven en `deliverables/` solo para probar.
- **Hipótesis vaga** que `040` no pueda validar: exigir marca `testeable_en` (aserción #4).

## 8. Siguiente paso

Tras **aprobar este diseño** (gate humano): **Planear** la celda en `710_plan/tracer-bullet/010_discovery.md`
(checklist de construcción), luego Ejecutar → Probar (fresco) → Verificar (fresco + gate).
