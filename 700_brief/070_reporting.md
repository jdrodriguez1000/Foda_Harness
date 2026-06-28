# Brief — Flujo 070 Reporting (Informe de negocio: márgenes, costo de oportunidad, inventario de seguridad)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `070` de 14 — `070_reporting` (decimotercer flujo de la tubería; **traduce** la demanda simulada a valor de negocio).
> **Posición en la tubería:** consume `060_simulation` (`simulation.json` / demanda simulada en gold) y, si aplica, `065_scenarios` (`scenarios.json`) → entrega el **informe al cliente**; `075_monitoring_alerting` vigila en operación.
> **Capa de datos que toca:** `gold` (lectura de demanda simulada / por escenario) + `bronze` (lectura de los parámetros financieros que entregó el cliente); **no escribe** capa — produce un informe.
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§11 Reporting) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el informe de una empresa concreta: describe la **maquinaria genérica y reutilizable** que, al
*operarse* sobre la demanda simulada de un cliente arbitrario, la **traduce a indicadores de negocio**
(márgenes, costo de oportunidad, costo del inventario de seguridad) y arma el **informe** que el cliente
recibe. El diseño **no debe cablear** precios ni costos: los parámetros financieros se **obtienen de la
información que el cliente entregó** (capa **bronze**), no del agente.

- **Insumo del flujo al operar:** la **demanda simulada** (`simulation.json` / gold) y, si aplica, la
  **demanda por escenario** (`scenarios.json`), más los **parámetros financieros** (precio unitario de venta,
  costo unitario de venta, costo de mantener inventario) **leídos de las tablas/datos que el cliente entregó
  en la capa bronze**. Cambia por cliente.
- **Salida de runtime que produce al operar:** el **`reporting.json`** (informe de negocio) y sus
  exportables. Pertenece al **plano instancia** (`fda-*`); **nunca** vuelve a la memoria de construcción del
  motor.
- **Grain del cliente (`D-014`):** los indicadores se calculan **por serie** (producto × geografía) y
  período, y pueden **agregarse** a niveles superiores (familia, sede, total) para la lectura ejecutiva.

## 1. Objetivo

Traducir la **demanda simulada** (y, si aplica, los **escenarios**) a **valor de negocio**: calcular, por
producto/sede y período, el **margen bruto esperado**, el **costo de oportunidad** y el **costo del
inventario de seguridad**, partiendo de los parámetros financieros (precio y costo unitario) que el cliente
entregó en la capa **bronze**.
El resultado es un **informe** (`reporting.json`) pensado para el cliente y el científico de datos, que cierra
la cadena predictiva con una lectura económica accionable.

> En una frase: transformar la **demanda simulada** + los **parámetros financieros** del cliente en un
> **informe de negocio** (`reporting.json`: márgenes, costo de oportunidad, inventario de seguridad),
> descargable y listo para la lectura ejecutiva.

## 2. Alcance — qué hace

**Modo Inicio (informe de negocio):**

- **Lectura de la demanda simulada:** toma la demanda simulada (`simulation.json` / gold) —y la demanda por
  escenario (`scenarios.json`) cuando se pida reportar escenarios— como base cuantitativa.
- **Incorporación de parámetros financieros:** toma el **precio unitario de venta**, el **costo unitario de
  venta** y el **costo de mantener inventario** **desde las tablas/datos que el cliente entregó en la capa
  bronze**.
- **Cálculo de indicadores de negocio:** por serie/período, calcula el **margen bruto esperado**, el **costo
  de oportunidad** y el **costo del inventario de seguridad** (sobre el inventario de seguridad derivado en
  Simulation).
- **Agregación para lectura ejecutiva:** consolida los indicadores a los niveles del grain que el cliente
  necesita (producto, familia, sede, total).
- **Armado del informe:** estructura todo en **`reporting.json`** (resumen de flujos anteriores, predicciones,
  simulaciones e indicadores económicos).
- **Entrega descargable:** permite al científico de datos descargar `reporting.json` en CSV o Excel.

## 3. Alcance — qué NO hace (límites)

- **No** genera el pronóstico ni el MAPE → flujo `055_inferences`.
- **No** corre la simulación Montecarlo ni deriva el inventario de seguridad → eso es el **flujo
  `060_simulation`** (Reporting **valoriza** su salida, no la recalcula).
- **No** parametriza escenarios "¿qué pasa si…?" → eso es el **flujo `065_scenarios`** (Reporting puede
  **reportar** sobre sus resultados, pero no los define).
- **No** monitorea la demanda real vs. la simulada ni emite alertas → eso es el **flujo
  `075_monitoring_alerting`**, que opera **después** del despliegue.
- **No** inventa precios ni costos: los parámetros financieros se **leen de la capa bronze** (datos del
  cliente), no se cablean.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas) → eso es el **diseño del flujo `070_reporting`**, paso
  siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición del flujo Reporting en la tubería FODA | `990_documents/expected_workflow.md` (§11) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de `simulation.json`, `scenarios.json` y del inventario de seguridad) | `700_brief/060_simulation.md`, `700_brief/065_scenarios.md` |

> **Insumo en tiempo de operación (no de construcción):** la **demanda simulada** real, los **escenarios** (si
> aplica) y los **parámetros financieros leídos de la capa bronze** (precio/costo unitario, costo de
> inventario, tal como el cliente los entregó). Llegan cuando el motor se *opera*, no ahora. (Para construir y
> probar el flujo se usa el **snapshot gold de C1** + el **snapshot bronze** con los campos financieros —
> `D-012`/`T-014`.)
>
> **Origen de los parámetros financieros (resuelto):** provienen de las **tablas/datos que el cliente
> entrega en la capa bronze**. No se introduce un insumo/YAML nuevo: el motor los **lee de bronze** (su
> mapeo se declara en Onboarding/`map_client_data.json` como cualquier otro campo del cliente).

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`reporting.json`** (informe de negocio) | Consolida demanda simulada + parámetros financieros en márgenes, costo de oportunidad y costo de inventario de seguridad, por serie/período y agregados. Es el **entregable al cliente** y soporta auditoría. |
| **Exportable CSV/Excel** de `reporting.json` | Permite al científico de datos descargar y compartir el informe con el cliente. |

> Los *paths*, el esquema exacto de `reporting.json`, las fórmulas precisas de cada indicador y el origen
> definitivo de los parámetros financieros se fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Se calculan, por **serie** y **período** (`D-014`), el **margen bruto esperado**, el **costo de
   oportunidad** y el **costo del inventario de seguridad**, a partir de la demanda simulada y los parámetros
   financieros.
2. Los parámetros financieros (precio, costo, costo de inventario) se **leen de la capa bronze** (datos
   entregados por el cliente), no cableados.
3. Los indicadores se **agregan** correctamente a los niveles del grain solicitados (producto/familia/sede/total).
4. **`reporting.json`** consolida el informe de forma **reproducible** y trazable hacia sus insumos
   (incluida la procedencia bronze de los parámetros financieros).
5. `reporting.json` es **descargable en CSV o Excel** para compartir con el cliente.
6. **Gate humano (si aplica):** el científico de datos **revisa/aprueba** el informe antes de entregarlo al
   cliente (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** `reporting.json` es **runtime de la instancia** (`fda-*`), no memoria de
  construcción.
- **Parámetros financieros ausentes en bronze:** si las tablas del cliente no traen precio/costo unitario o
  costo de inventario, no hay márgenes. Conviene que **Profiling/Onboarding** verifiquen su presencia y
  mapeo; cablearlos en el agente rompe la reutilización (son **dato de bronze**, no código).
- **Hereda errores aguas arriba:** Reporting valoriza la demanda simulada; un MAPE/simulación erróneos
  producen un informe económico engañoso. (Riesgo aguas arriba; aquí se asume el contrato de `060`/`065`.)
- **Mezcla de niveles de agregación:** sumar márgenes entre series con distinto precio/costo sin respetar el
  grain produce cifras incorrectas; agregar con cuidado (`D-014`).
- **Informe sin trazabilidad:** un `reporting.json` que no enlaza con sus insumos (predicción, simulación,
  parámetros) no es auditable. Mantener la trazabilidad.
- **Confundir Reporting con Monitoring:** Reporting es el informe **predictivo/económico** previo;
  `075_monitoring_alerting` compara contra la **demanda real** en operación. No solaparlos.

## 8. La traducción a valor de negocio — sección específica del flujo

Reporting es el flujo donde la tubería **deja de hablar de unidades y empieza a hablar de dinero**:

- **Indicadores objetivo** (de la fuente §11), por producto/período: **precio unitario de venta**, **costo
  unitario de venta**, **costo del inventario de seguridad**, **margen bruto esperado** y **costo de
  oportunidad**. Ejemplo ilustrativo de la fuente:

  | Período | Precio unit. venta | Costo unit. venta | Costo Seguridad | Margen Bruto Esperado | Costo Oportunidad |
  |---------|--------------------|--------------------|-----------------|------------------------|-------------------|
  | 1 | $65.300 | $48.600 | $9.006.240 | $17.735.400 | $3.094.737 |
  | 2 | $65.300 | $48.600 | $13.011.879 | $28.557.000 | $4.471.160 |
  | 3 | $65.300 | $48.600 | $14.009.360 | $24.866.300 | $4.813.916 |

- **Dependencia de Simulation.** El **costo del inventario de seguridad** se calcula sobre el inventario de
  seguridad que **derivó Simulation**; el **costo de oportunidad** y el **margen** dependen de la demanda
  simulada (y de los escenarios, si se reportan). Reporting **valoriza**, no recalcula la demanda.
- **Parámetros financieros como dato de bronze.** Precio y costo unitario, y costo de mantener inventario,
  vienen en las **tablas que el cliente entrega** (capa **bronze**); el motor los **lee** de ahí (su mapeo se
  declara en Onboarding/`map_client_data.json`). No se cablean ni se piden por un insumo aparte.
- **Audiencia doble.** El informe sirve al **cliente** (lectura ejecutiva, agregada) y al **científico de
  datos** (detalle por serie, auditoría). El diseño debe contemplar ambas vistas.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Reporting (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): margen básico sobre C1 con precio/costo fijos de fixture. Cada peldaño
> agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Margen bruto básico (1 serie)** | Toma la demanda simulada de una serie de C1 + precio/costo unitario de un fixture, calcula el **margen bruto esperado** por período y arma un `reporting.json` mínimo. | Una serie; solo margen (sin costo de oportunidad ni costo de inventario); parámetros de fixture; sin exportación; sin agregación. |
| **L1** | **Set completo de indicadores + multi-serie + bitácora** | Calcula margen, **costo de oportunidad** y **costo de inventario de seguridad** para todas las series; `reporting.json` consolida el informe. | Parámetros financieros aún de fixture; sin agregación jerárquica; sin exportación. |
| **L2** | **Agregación jerárquica + parámetros desde bronze + exportable** | Agrega a familia/sede/total; parámetros financieros **leídos de la capa bronze** del cliente (mapeados en Onboarding); descarga CSV/Excel. | Sin reporte de escenarios; vista ejecutiva básica. |
| **L3** | **Reporte de escenarios + vistas ejecutiva/detalle + replay** | Incorpora `scenarios.json` (base vs. escenarios) al informe; vistas separadas para cliente y científico de datos; replay reproducible; gate de aprobación del informe. | Sin narrativa/insights automáticos avanzados. |
| **Ln** (ambición completa) | **Reporting "como un científico de datos senior"** | Informe económico completo (márgenes, costo de oportunidad, inventario de seguridad) multi-serie y multi-nivel, con escenarios, vistas ejecutiva y de detalle, narrativa de insights, exportables ricos y trazabilidad total hacia los insumos. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Reporting: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `070_reporting`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, durabilidad, rúbrica del evaluador y
contrato), reutilizando los patrones transversales ya validados del motor, **leyendo los parámetros
financieros de la capa bronze** (mapeados en Onboarding). El **plan de implementación** viene *después* del diseño (orden
del método: **brief → diseño → plan → construir**, `D-011`). El diseño se materializará en
`705_design/070_reporting.md`.
