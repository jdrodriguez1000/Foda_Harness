# Brief — Flujo 030 Cleaning (Limpieza → capa silver)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `030` de 14 — `030_cleaning` (quinto flujo de la tubería; primer flujo de **transformación**: produce la capa silver).
> **Posición en la tubería:** consume `025_profiling` (informe de salud) + capa **bronze** (`020_ingestion`) → entrega a `035_derivation`.
> **Capa de datos que toca:** `bronze` (lectura) → **escribe** `silver` (datos limpios).
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§5 Cleaning) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `BORRADOR` · **Fecha:** `2026-06-28` · **Aprobado por:** `—`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe la limpieza de una empresa concreta: describe la **maquinaria genérica y reutilizable** que,
al *operarse* sobre la capa bronze de un cliente arbitrario, aplica un **conjunto de reglas de limpieza
declaradas por el humano** (`data_cleaner.yaml`) y produce una capa **silver** limpia, documentando cada
transformación. El diseño no debe acoplarse a un dominio ni cablear reglas fijas: las reglas son **dato de
entrada**, no código.

- **Insumo del flujo al operar:** la capa **bronze** del cliente, el **informe de salud** (de Profiling)
  y el **`data_cleaner.yaml`** (reglas de limpieza co-construidas por el científico de datos y el
  cliente). Cambia por cliente.
- **Salida de runtime que produce al operar:** la capa **silver** (datos limpios) y el
  **`data_cleaning.json`** (bitácora de transformaciones, replicable). Pertenecen al **plano instancia**
  (`fda-*`); **nunca** vuelven a la memoria de construcción del motor.
- **Grain del cliente (`D-014`):** la limpieza **preserva** el grain (producto × geografía); silver
  conserva las mismas series que bronze, sin agregar (eso es Derivation). Las reglas pueden aplicarse
  por campo y, en niveles maduros, condicionadas por segmento/nivel.

## 1. Objetivo

Transformar la capa **bronze** (cruda, con errores) en una capa **silver** limpia y lista para derivar,
aplicando **reglas de limpieza explícitas y aprobadas por el humano** y **documentando cada
transformación** para que el proceso sea **reproducible y auditable**. Cleaning **no inventa reglas ni
decide a ciegas**: ejecuta el `data_cleaner.yaml` que el científico de datos construye con el cliente
(orientado por el informe de Profiling), y deja trazabilidad bronze→silver.

> En una frase: transformar **bronze** en una capa **silver** aplicando el `data_cleaner.yaml`, y
> registrar el detalle en `data_cleaning.json` para Derivation.

## 2. Alcance — qué hace

**Modo Inicio (limpieza de la carga):**

- **Toma de las reglas de limpieza:** lee el **`data_cleaner.yaml`** (autoría humana, ver §8) que define
  cómo proceder ante cada problema, p. ej.:
  - **Faltante numérico** → imputar **media/mediana**.
  - **Faltante categórico** → imputar **moda**.
  - **Faltante de fecha** → imputar **fecha más cercana**.
  - **Duplicado** → eliminar el duplicado.
  - **Inconsistente / desactualizado / incompleto** → eliminar el registro.
- **Aplicación de las reglas:** ejecuta las reglas sobre la capa bronze, sin alterar bronze (lo lee).
- **Escritura de silver:** deposita el resultado **limpio** en la capa **silver**, lista para Derivation.
- **Bitácora de transformaciones:** registra qué se hizo en **`data_cleaning.json`** (qué regla, a qué
  campos/registros, con qué efecto): documenta y **permite replicar** la limpieza en otros archivos del
  cliente.
- **Entrega descargable:** permite al científico de datos descargar `data_cleaning.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** diagnostica la salud ni prioriza problemas → eso es el **flujo `025_profiling`** (que Cleaning
  consume como guía).
- **No** modifica **bronze** → bronze es inmutable (`020_ingestion`); la limpieza vive en silver.
- **No** agrega ni deriva la demanda (no calcula demanda semanal/mensual…) → eso es el **flujo
  `035_derivation`** (capa gold).
- **No** crea variables nuevas (feature engineering) → eso son los flujos `040_exploration` /
  `045_featuring`.
- **No** **decide** las reglas por su cuenta: el `data_cleaner.yaml` es **autoría humana** (científico de
  datos + cliente). En niveles maduros Cleaning puede **sugerir** reglas, pero la aprobación es humana.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `030_cleaning`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Cleaning en la tubería FODA | `990_documents/expected_workflow.md` (§5) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de bronze y del informe de salud) | `700_brief/020_ingestion.md`, `700_brief/025_profiling.md` |

> **Insumo en tiempo de operación (no de construcción):** la capa **bronze real**, el informe de salud y
> el **`data_cleaner.yaml`** co-construido con el cliente. Llegan cuando el motor se *opera*, no ahora.
> (Para construir y probar el flujo se usa el **snapshot bronze de C1** + un `data_cleaner.yaml` fixture —
> `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **Capa `silver`** (datos limpios) | Datos limpios y consistentes, listos para derivar la demanda. La consume `035_derivation` (origen del cálculo de demanda hacia gold). |
| **`data_cleaning.json`** (bitácora de transformaciones) | Documenta cada transformación aplicada; habilita **reproducir** la limpieza en otros archivos del cliente y auditar bronze→silver. |
| **Exportable CSV/Excel** de `data_cleaning.json` | Permite al científico de datos descargar y compartir el detalle de la limpieza. |

> El **`data_cleaner.yaml`** es **insumo** (autoría humana), no salida de este flujo. Los *paths*, el
> esquema exacto de `data_cleaning.json` y la mecánica se fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Existe un **`data_cleaner.yaml`** aprobado por el humano y las reglas se **aplicaron** sobre bronze.
2. La capa **silver** queda escrita con datos limpios coherentes con las reglas; **bronze no se alteró**.
3. Cada transformación queda registrada en **`data_cleaning.json`** (regla, alcance, efecto), de forma que
   el proceso sea **reproducible** sobre otros archivos del cliente.
4. El **grain** (producto × geografía) se preserva: silver mantiene las mismas series que bronze (`D-014`).
5. `data_cleaning.json` es **descargable en CSV o Excel**.
6. **Gate humano (central):** el científico de datos (con el cliente) **construye/aprueba** el
   `data_cleaner.yaml` antes de ejecutar la limpieza (ver `CLAUDE.md §5`). Es el punto de decisión clave
   de este flujo.

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** silver y `data_cleaning.json` son **runtime de la instancia**
  (`fda-*`), no memoria de construcción.
- **Reglas cableadas (anti-patrón):** hard-codear reglas en el agente en vez de leerlas del
  `data_cleaner.yaml` rompe la reutilización y el control humano. Las reglas son **dato**, no código.
- **Envenenar aguas abajo (E9):** una limpieza agresiva (eliminar demasiados registros) o una imputación
  inadecuada **distorsiona la demanda** que Derivation calculará y el modelo aprenderá. La autoría humana
  del yaml y la bitácora auditable son la mitigación.
- **Pérdida de trazabilidad:** limpiar sin registrar en `data_cleaning.json` impide reproducir y auditar;
  cada transformación debe quedar documentada.
- **Imputación que falsea la señal:** imputar faltantes con la media puede aplanar estacionalidad real;
  las reglas deben ser conscientes del dominio (lo decide el humano).
- **Snapshot stale (al construir):** silver de C1 depende del snapshot bronze y del `data_cleaner.yaml`
  fixture; si cambian, regenerar (`D-012`).

## 8. `data_cleaner.yaml` (autoría humana) + `data_cleaning.json` (bitácora replicable) — sección específica del flujo

Cleaning es el flujo donde el **control humano** y la **trazabilidad** son el corazón del diseño:

- **`data_cleaner.yaml` — el contrato de limpieza (entrada, autoría humana):** lo construye el científico
  de datos **con el cliente**, orientado por el informe de Profiling. Declara, por tipo de problema y por
  campo, **qué hacer** (imputar media/mediana/moda/fecha-cercana, eliminar duplicado/registro…). Es el
  **gate humano** del flujo: la IA **no decide** las reglas, las **ejecuta**. Separar reglas (dato) de
  ejecución (agente) es lo que hace el flujo reutilizable entre clientes.
- **`data_cleaning.json` — la bitácora (salida, replicable):** registra cada transformación aplicada. Dos
  propósitos: **auditar** la transición bronze→silver (qué cambió y por qué) y **replicar** la misma
  limpieza en cargas/archivos futuros del cliente sin rehacer el análisis. Es la trazabilidad que exige
  `CLAUDE.md §5`.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Cleaning (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): aplicar un `data_cleaner.yaml` mínimo sobre el snapshot bronze de
> C1 y escribir silver. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Aplicar reglas mínimas → silver + bitácora básica** | Lee un `data_cleaner.yaml` fixture con 1–2 reglas (p. ej. imputar faltante numérico con la media, eliminar duplicados), las aplica sobre el snapshot bronze de C1, escribe **silver** y un `data_cleaning.json` básico; handoff a Derivation. | yaml pre-provisto (no co-construido en vivo); pocas reglas; sin exportación; sin reglas por grain. |
| **L1** | **Conjunto completo de reglas + bitácora completa** | Cubre todas las reglas de la fuente (imputación media/mediana/moda/fecha-cercana; eliminación de duplicados/inconsistentes/desactualizados/incompletos); `data_cleaning.json` documenta cada transformación. | yaml aún pre-provisto; sin exportación; sin validación de mejora de salud. |
| **L2** | **Co-autoría del yaml (gate) + exportable + replay** | Construcción/aprobación interactiva del `data_cleaner.yaml` con el humano; exportación a CSV/Excel; replicabilidad de la limpieza validada sobre otra carga. | Reglas globales (no segmentadas por grain); sin re-perfilado posterior. |
| **L3** | **Reglas por grain/segmento + validación de mejora** | Reglas condicionadas por nivel/segmento (familia/sede); tras limpiar, **re-perfila** para validar que la salud mejoró; replay idempotente entre cargas. | Reglas sugeridas aún manuales; sin imputación por modelos. |
| **Ln** (ambición completa) | **Cleaning "como un científico de datos senior"** | Sugerencia automática de reglas a partir del informe de Profiling (aprobadas por el humano), imputación avanzada (por modelos/series temporales), tratamiento de outliers consciente de estacionalidad, replay robusto y versionado entre cargas. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Cleaning: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `030_cleaning`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor. El **plan de implementación**
viene *después* del diseño (orden del método: **brief → diseño → plan → construir**, `D-011`). El diseño
se materializará en `705_design/030_cleaning.md`.
