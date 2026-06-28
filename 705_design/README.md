# 705_design — Diseñar (output del paso *Diseñar*)

> Carril del paso **Diseñar** del ciclo de construcción por vertical slice (`D-021`).

## Qué guarda
El **diseño técnico por celda** (flujo × banda): cómo se va a construir el peldaño L de ese
flujo en esa banda. Es el paso que sigue a *Definir* (`703_definition/`) y antecede a *Planear*
(`710_plan/`).

## Convención
```
705_design/<banda>/<flujo>.md
```
- `<banda>` ∈ `tracer-bullet`, `stabilization`, `mvp`, `evolution`, `final` (`D-017`).
- `<flujo>` = nombre canónico del flujo (`010_discovery` … `075_monitoring`), ver `700_brief/`.
- **Un archivo `.md` por celda**, no una carpeta. Se crea cuando esa celda entra en diseño.

## Notas
- En el **Tracer Bullet** el diseño por celda es **ligero** (E4): el peso del alcance está en el
  `slice_contract` de la banda (`703_definition/tracer-bullet/`). Ver `D-021 §4`.
- Insumos del diseño de una celda: su **brief** (`700_brief/<flujo>.md`, la escalera L0→Ln) +
  el **`slice_contract`** de la banda (qué peldaño entra) + `000_general_process.md` (contratos I/O).
