# Plan de construcción — `010_discovery` × Tracer Bullet (L0)

> **Paso:** Planear (`D-029`, `methodology.md §7`). Es un **checklist de construcción** (E4), no un diseño.
> **Insumo:** `705_design/tracer-bullet/010_discovery.md` (diseño `APROBADO` 2026-07-01).
> **Destino de la construcción:** `720_build/tracer-bullet/010_discovery/`.
> **Estado:** `PROPUESTO` · **Fecha:** `2026-07-01`.

---

## 1. Orden de construcción (Ejecutar)

Se construye **contrato → schema → skill → agente**, para que cada pieza apoye en la anterior (el agente
es lo último porque consume schema y skill).

| # | Artefacto a crear | Ruta | Notas |
|---|-------------------|------|-------|
| 1 | `cell_contract.md` | `contract/` | Done de la celda + las 7 aserciones RED del diseño §5. Fuente de verdad de "terminado". |
| 2 | `contract_data.schema.json` | `schemas/` | JSON Schema (draft-07). Campos obligatorios: `archivos_esperados[]`, `medio_acceso`, `periodicidad`, `horizonte_meses`, `grain.producto[]`, `grain.geografia[]`, `financieros_en_fuente[]`. |
| 3 | `validate_discovery.py` | `skills/` | Python stdlib + `pyyaml` + `jsonschema`. CLI: `python validate_discovery.py --deliverables <dir> --schema <path> --report <out>`. Determinista (sin red, sin timestamps en el veredicto). |
| 4 | `foda-discovery.md` | `agents/` | Definición del worker (frontmatter `tools: Read, Write, Bash`; sin `Agent`). Instrucciones: leer los 2 cuestionarios → emitir los 3 artefactos en `deliverables/` → invocar la skill (Bash) → reportar path del `validation_report.json`. |

## 2. Detalle por artefacto

### 1) `contract/cell_contract.md`
- [ ] Encabezado: flujo/banda/peldaño, capa `—`, insumos, salidas.
- [ ] **Done L0** (del brief §6 acotado a L0): 3 artefactos bien formados + consistentes; grain+periodicidad inequívocos; ≥1 hipótesis testeable; ≥3 áreas; gate humano.
- [ ] **Aserciones RED** = las 7 del diseño §5 (numeradas, verificables por la skill o por inspección humana).

### 2) `schemas/contract_data.schema.json`
- [ ] `$schema` draft-07, `type: object`, `required` con los 7 campos.
- [ ] `medio_acceso` enum `["csv","base_de_datos","api"]`; `periodicidad` enum (semanal…anual).
- [ ] `grain.producto` / `grain.geografia` = arrays de strings no vacíos; `horizonte_meses` entero ≥1.
- [ ] `archivos_esperados` = array de objetos `{nombre, naturaleza, medio}`.

### 3) `skills/validate_discovery.py`
- [ ] Carga los 3 artefactos desde `--deliverables`.
- [ ] Valida `contract_data.json` contra el schema (`jsonschema`).
- [ ] Parsea `client_register.yaml`; chequea campos mínimos (§4 diseño).
- [ ] **Consistencia registro⇄contrato:** `periodicidad`, niveles de `grain`, sede y nº SKUs coinciden.
- [ ] Cuenta hipótesis con marca `testeable_en` en `business_hypothesis.md` (regex) → ≥1.
- [ ] Cuenta `areas_entrevistadas` distintas → ≥3.
- [ ] Escribe `evaluation/validation_report.json`: `{ "ok": bool, "checks": [...], "hallazgos": [...] }` **sin timestamp** (determinismo, aserción #6).
- [ ] Exit code 0 si `ok`, 1 si falla (para el paso Probar).

### 4) `agents/foda-discovery.md`
- [ ] Frontmatter: `name: foda-discovery`, `tools: Read, Write, Bash` (`Bash` para correr la skill), `model` a criterio de A.
- [ ] Rol: worker de síntesis; **no** spawnea (modelo plano `D-009`).
- [ ] Procedimiento: (a) leer ambos cuestionarios; (b) redactar `client_register.yaml`; (c) `business_hypothesis.md` (≥1 hipótesis con `testeable_en`); (d) `contract_data.json` conforme al schema; (e) correr la skill; (f) reportar solo el path del reporte (E6).
- [ ] Recordatorio de planos: los deliverables son `fda-*`; aquí se emiten a `deliverables/` solo para probar.

## 3. Dependencias / ambiente

- [ ] Python disponible (ya verificado en T-014). Añadir `jsonschema` y `pyyaml` si faltan (`pip`).
- [ ] No requiere Postgres (Discovery no toca capas de datos).
- [ ] Ruta de entrada fija al golden client C1 (los 2 cuestionarios).

## 4. Cómo se probará (anticipo del paso Probar, contexto fresco)

1. Ejecutar el agente `foda-discovery` sobre los cuestionarios de C1 → produce los 3 artefactos.
2. Correr `validate_discovery.py` → `validation_report.json` con `ok: true`.
3. Reejecutar la validación → reporte idéntico (determinismo, aserción #6).
4. Verificación en **contexto fresco** (TR-2) contra `cell_contract.md`, `slice_contract §2 fila 010` y brief L0.

## 5. Siguiente paso

Tras este plan: **Ejecutar** — construir los 4 artefactos en el orden de §1 dentro de
`720_build/tracer-bullet/010_discovery/`.
