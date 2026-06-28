# Brief — Flujo 075 Monitoring (Vigilancia en operación: real vs. simulado + alertas)

> **Tipo:** Brief de enmarque (alto nivel, previo al diseño agéntico). NO es la definición agéntica fina.
> **Proyecto:** FODA (Forecast Optimization Driven Agentic) — plano de **construcción** del motor.
> **Flujo:** `075` de 14 — `075_monitoring` (decimocuarto y último flujo; agrupa **Monitoring** + **Alerting** de la fuente). Opera **después** del despliegue, de forma recurrente.
> **Posición en la tubería:** consume la **demanda real** del cliente + la **demanda simulada** (`060_simulation` / gold) y el pronóstico (`055_inferences`) → produce vigilancia y alertas; puede **disparar re-ejecución** aguas arriba.
> **Capa de datos que toca:** `gold` (lectura de demanda simulada/pronosticada) + `bronze` (lectura de la demanda real que el cliente entrega); **no escribe** capa — produce informes/alertas.
> **Fuente de verdad:** `990_documents/expected_workflow.md` (§12 Monitoring + §13 Alerting) + `990_documents/expected_solution.md`.
> **Método de construcción:** `950_guideline/methodology.md` + `950_guideline/principles.md`.
> **Decisiones que lo enmarcan:** `D-001` (dos planos), `D-012` (snapshots), `D-014` (grain producto × geo), `D-015` (walking skeleton), `D-016` (brief + escalera), `D-017` (bandas + numeración) · **Estado:** `APROBADO` · **Fecha:** `2026-06-28` · **Aprobado por:** `usuario`.

---

## 0. Aclaración de planos — leer primero

Este brief describe un **componente del MOTOR FODA que estamos fabricando** (plano de *construcción*).
No describe el monitoreo de una empresa concreta: describe la **maquinaria genérica y reutilizable** que, al
*operarse*, compara de forma recurrente la **demanda real** de un cliente arbitrario contra la **demanda
simulada/pronosticada**, mide la desviación y **alerta** cuando supera un umbral configurable. El diseño
**no debe cablear** umbrales ni rutas de notificación: son **dato de entrada**.

- **Insumo del flujo al operar:** la **demanda real** (que el cliente entrega periódicamente, en **bronze**),
  la **demanda simulada/pronosticada** (`simulation.json` / `inferences.json` / gold) y la **configuración de
  alertas** (umbral de desviación, destinatarios). Cambia por cliente.
- **Salida de runtime que produce al operar:** el **`monitoring.json`** (seguimiento de la calidad) y el
  **`alerting.json`** (alertas emitidas). Pertenecen al **plano instancia** (`fda-*`); **nunca** vuelven a la
  memoria de construcción del motor.
- **Grain del cliente (`D-014`):** la comparación real vs. simulado se hace **por serie** (producto ×
  geografía) y período; las alertas pueden emitirse por serie o agregadas según la configuración.

## 1. Objetivo

**Cerrar el ciclo** de la tubería vigilando, ya en operación, qué tan bien predijo el sistema: comparar la
**demanda real** contra la **demanda simulada/pronosticada**, cuantificar la desviación por serie/período y
**emitir alertas** cuando esa desviación supera el umbral definido. Es el flujo que mantiene viva la solución
en el tiempo: detecta degradación del modelo y, cuando corresponde, **señala la necesidad de re-ejecutar**
flujos aguas arriba (re-inferencia, re-simulación o re-modelado).

> En una frase: transformar la **demanda real** + la **demanda simulada** en un **seguimiento de calidad**
> (`monitoring.json`) y **alertas** (`alerting.json`) que avisan cuando la desviación supera el umbral.

## 2. Alcance — qué hace

**Sub-flujo Monitoring (seguimiento de calidad):**

- **Lectura de la demanda real:** toma la demanda real que el cliente entrega periódicamente (capa **bronze**).
- **Comparación real vs. simulado/pronosticado:** confronta la real contra la demanda simulada/pronosticada
  (gold), por serie/período, y calcula la **desviación** (p. ej. error vs. el MAPE esperado).
- **Bitácora de monitoreo:** registra el seguimiento en **`monitoring.json`** (desviación por serie/período,
  evolución de la calidad), documentado y **replicable**.
- **Entrega descargable:** permite al científico de datos descargar `monitoring.json` en CSV o Excel.

**Sub-flujo Alerting (alertas):**

- **Evaluación de umbral:** compara la desviación contra el **umbral configurado**; cuando la real se aparta
  de la simulada más de lo permitido, marca la condición de alerta.
- **Emisión de alertas:** genera **`alerting.json`** con las alertas (serie, período, magnitud de la
  desviación) para avisar al cliente / científico de datos.
- **Señal de re-ejecución (si aplica):** cuando la degradación es persistente, **señala** la conveniencia de
  re-ejecutar flujos aguas arriba (re-inferencia / re-simulación / re-modelado) — sin ejecutarlos él mismo.

## 3. Alcance — qué NO hace (límites)

- **No** genera el pronóstico ni el MAPE → flujo `055_inferences`.
- **No** corre la simulación → flujo `060_simulation`.
- **No** re-entrena ni re-modela por su cuenta → eso son los flujos `050`/`055`/`060` cuando se **re-ejecutan**;
  Monitoring **detecta y señala** la necesidad, no la ejecuta.
- **No** produce el informe económico → flujo `070_reporting`.
- **No** inventa la demanda real: la **lee de bronze** (dato que el cliente entrega), no la fabrica.
- **No** define umbrales ni destinatarios de alerta cableados → son **configuración** (dato), no código.
- **No** diseña la **maquinaria agéntica fina** de este flujo (instancias A/B/C, workers, checkpoints,
  rúbrica del evaluador, contratos de herramientas, scheduling) → eso es el **diseño del flujo
  `075_monitoring`**, paso siguiente a este brief.

## 4. Insumos disponibles

| ID | Insumo | Origen |
|----|--------|--------|
| I-1 | Definición de Monitoring + Alerting en la tubería FODA | `990_documents/expected_workflow.md` (§12, §13) |
| I-2 | Arquitectura de capas bronze/silver/gold y visión de planos | `990_documents/expected_solution.md`, `CLAUDE.md §4` |
| I-3 | Metodología y principios de construcción (P*, E*, NC*, patrón A/B/C, modelo plano) | `950_guideline/methodology.md`, `950_guideline/principles.md` |
| I-4 | Memoria de construcción (estado, decisiones, lecciones) | `800_persistence/` (`D-001`, `D-012`, `D-014`, `D-017`) |
| I-5 | Briefs aprobados aguas arriba (forma de `inferences.json`, `simulation.json` y del MAPE) | `700_brief/055_inferences.md`, `700_brief/060_simulation.md` |

> **Insumo en tiempo de operación (no de construcción):** la **demanda real** del cliente (bronze), la
> **demanda simulada/pronosticada** (gold) y la **configuración de alertas** (umbral, destinatarios). Llegan
> cuando el motor se *opera* de forma recurrente, no ahora. (Para construir y probar el flujo se usa el
> **snapshot gold de C1** + un fixture de **demanda real** desfasada y un umbral de prueba — `D-012`/`T-014`.)

## 5. Artefactos esperados (salida del flujo al operar)

| Artefacto | Propósito |
|-----------|-----------|
| **`monitoring.json`** (seguimiento de calidad) | Desviación real vs. simulado por serie/período y su evolución; soporta auditoría y la decisión de re-ejecutar. |
| **`alerting.json`** (alertas emitidas) | Alertas cuando la desviación supera el umbral (serie, período, magnitud); avisa al cliente / científico de datos. |
| **Exportable CSV/Excel** de `monitoring.json` | Permite al científico de datos descargar y compartir el seguimiento. |

> Los *paths*, el esquema exacto de `monitoring.json` / `alerting.json`, la política de umbrales y el
> mecanismo de notificación se fijan en el **diseño del flujo** (paso siguiente).

## 6. Criterios de éxito (Done)

1. Se compara la **demanda real** (bronze) contra la **demanda simulada/pronosticada** (gold) por **serie** y
   **período** (`D-014`), calculando la desviación.
2. **`monitoring.json`** registra la desviación y su evolución de forma **reproducible**.
3. Se evalúa la desviación contra un **umbral configurable**; al superarlo se genera **`alerting.json`** con
   la alerta correspondiente.
4. Umbral y destinatarios entran como **configuración** (dato), no cableados.
5. Cuando la degradación lo amerita, el flujo **señala** la necesidad de re-ejecutar flujos aguas arriba (sin
   ejecutarlos).
6. `monitoring.json` es **descargable en CSV o Excel**.
7. **Gate humano (si aplica):** el científico de datos **revisa** las alertas y **decide** la re-ejecución
   (ver `CLAUDE.md §5`).

## 7. Riesgos / advertencias

- **Confusión de planos (`D-001`):** `monitoring.json` y `alerting.json` son **runtime de la instancia**
  (`fda-*`), no memoria de construcción.
- **Comparar mal real vs. simulado:** alinear períodos/series incorrectamente (o comparar contra el escenario
  equivocado) produce desviaciones falsas y alertas erróneas. Respetar el grain y el período (`D-014`).
- **Umbral cableado o mal calibrado:** un umbral fijo en el agente rompe la reutilización; uno mal calibrado
  genera **fatiga de alertas** (demasiadas) o **silencio peligroso** (degradación no detectada). Es **dato**
  configurable.
- **Demanda real ausente/tardía:** sin la real en bronze no hay monitoreo; el flujo debe degradar con gracia
  cuando aún no llega el período real.
- **Re-ejecutar sin control:** disparar re-modelado automático sin gate humano puede desestabilizar la
  solución; Monitoring **señala**, el humano **decide** (`CLAUDE.md §5`).
- **Cierre del ciclo:** este flujo realimenta a `050`/`055`/`060`; un monitoreo erróneo puede inducir
  re-ejecuciones innecesarias o impedir las necesarias. Trazabilidad en `monitoring.json` mitiga.

## 8. Cierre del ciclo: monitorear para realimentar — sección específica del flujo

`075_monitoring` es el flujo que convierte la tubería **lineal** en un **ciclo vivo**:

- **Dos sub-flujos, un propósito.** **Monitoring** mide (real vs. simulado); **Alerting** avisa (umbral
  superado). Se redactan juntos en este brief por su acoplamiento, pero producen artefactos distintos
  (`monitoring.json`, `alerting.json`).
- **Naturaleza recurrente.** A diferencia de los flujos `010`–`070` (que corren una vez por construcción de la
  solución), Monitoring corre **periódicamente** a medida que el cliente entrega demanda real. El diseño debe
  contemplar **scheduling/recurrencia** y la llegada incremental de la real en bronze.
- **Realimentación con gate humano.** Cuando la calidad cae, el valor del flujo es **señalar** la
  re-ejecución de flujos aguas arriba (re-inferencia, re-simulación o re-modelado). La decisión de re-ejecutar
  la **aprueba el científico de datos**, fiel al principio de "el humano aprueba" (`CLAUDE.md §5`).
- **Umbral como configuración.** El "porcentaje definido" de la fuente (§13) es un **parámetro** del cliente;
  tratarlo como dato permite ajustar la sensibilidad de las alertas sin tocar el motor.

## 9. Escalera de capacidades (L0 → Ln) — vista vertical del flujo

> Vista vertical de la *ambición completa* de Monitoring (`D-016`). **L0 = lo mínimo** del walking skeleton
> (banda **Tracer Bullet**, `D-017`): comparar real vs. simulado en una serie de C1 y alertar con un umbral
> fijo. Cada peldaño agrega capacidad.

| Nivel | Capacidad | Qué incluye | Qué difiere de la realidad |
|-------|-----------|-------------|----------------------------|
| **L0** (mínimo / skeleton) | **Comparar real vs. simulado + alerta básica (1 serie)** | Lee una demanda real fixture y la simulada de una serie de C1, calcula la desviación, escribe un `monitoring.json` básico y, si supera un umbral fijo, un `alerting.json` mínimo. | Una serie; umbral fijo; sin recurrencia/scheduling; sin notificación real; sin señal de re-ejecución; sin exportación. |
| **L1** | **Multi-serie + umbral configurable + bitácora completa** | Monitorea todas las series del grain; umbral leído de configuración; `monitoring.json` con evolución y `alerting.json` con alertas por serie/período. | Sin recurrencia automática; notificación simple; sin señal de re-ejecución. |
| **L2** | **Recurrencia + exportable + señal de re-ejecución** | Corre periódicamente con la real incremental de bronze; descarga CSV/Excel; **señala** la conveniencia de re-ejecutar flujos aguas arriba. | Re-ejecución manual; sin políticas de alerta avanzadas. |
| **L3** | **Notificación + políticas de alerta + gate de re-ejecución formal** | Canales de notificación configurables (destinatarios); políticas anti-fatiga (agrupación, severidad); gate humano formal para aprobar re-ejecución. | Sin auto-remediación; catálogo de métricas acotado. |
| **Ln** (ambición completa) | **Monitoring "como un científico de datos senior"** | Vigilancia recurrente multi-serie/multi-nivel, métricas de degradación ricas, umbrales y políticas de alerta calibrables, notificación multicanal, realimentación al ciclo (re-inferencia/re-modelado) con gate humano, todo trazable y ligado al contrato. | Nada: es el objetivo final del flujo. |

> **Nota de ensamblaje:** al cerrar este brief se refleja el estado en `800_persistence/roadmap.md`
> (fila Monitoring: columna *Brief* → `planeado`; peldaño previsto para Tracer Bullet → **L0**).

## 10. Siguiente paso

Tras **aprobar este brief**: **diseñar el flujo `075_monitoring`** (instancias A/B/C según el modelo plano
`D-009`, workers, política de herramientas, checkpoints canónicos, **recurrencia/scheduling**, durabilidad,
rúbrica del evaluador y contrato), reutilizando los patrones transversales ya validados del motor. El **plan
de implementación** viene *después* del diseño (orden del método: **brief → diseño → plan → construir**,
`D-011`). El diseño se materializará en `705_design/075_monitoring.md`.
