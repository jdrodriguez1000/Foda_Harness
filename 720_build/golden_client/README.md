# golden_client — Cliente de prueba canónico C1 + snapshots

> Infraestructura de construcción del MOTOR para probar la tubería **sin re-ejecutar toda la cadena**
> en cada celda (`D-012` híbrido). Carril compartido entre bandas.

## Qué guarda
- **El golden client C1**: cliente de prueba canónico generado por el **generador sintético
  parametrizado** por jerarquía producto/geo y nº de series (`D-014`). C1 = 1 sede × ~5–10 SKUs,
  mensual, ~24–36 meses, con **hold-out de Monitoring** (K períodos).
- **`snapshots/`**: congelado de las capas **bronze/silver/gold** y de los artefactos por flujo, de
  modo que cada celda parta del output cacheado de la anterior. El snapshot se **versiona ligado al
  contrato upstream** (si cambia el contrato del flujo previo, se invalida el snapshot).

## Notas
- Aprovecha la **inmutabilidad** bronze → silver → gold (`D-012`).
- Fixtures escalonados (`D-014`): **C1 primario ya**; C4 (estrés) y C2/C3 bajo demanda.
- **Construir esta infraestructura es la tarea `T-014`** — prerrequisito de la primera celda
  (`010_discovery`) del Tracer Bullet.
