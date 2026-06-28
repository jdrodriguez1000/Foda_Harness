# 710_plan — Planear (output del paso *Planear*)

> Carril del paso **Planear** del ciclo de construcción por vertical slice (`D-021`).

## Qué guarda
El **plan de ejecución por celda** (flujo × banda): pasos concretos, orden, archivos a tocar y
criterios de aceptación para construir el diseño (`705_design/`) de esa celda. Antecede a
*Ejecutar/Probar/Verificar* (`720_build/`).

## Convención
```
710_plan/<banda>/<flujo>.md
```
- `<banda>` ∈ `tracer-bullet`, `stabilization`, `mvp`, `evolution`, `final` (`D-017`).
- `<flujo>` = nombre canónico del flujo (`010_discovery` … `075_monitoring`), ver `700_brief/`.
- **Un archivo `.md` por celda**, no una carpeta. Se crea cuando esa celda entra en planeación.

## Notas
- En el **Tracer Bullet** el plan por celda es **ligero** (E4). Ver `D-021 §4`.
- **Importante (enmienda `D-021 §4` / `L-010`):** el `slice_contract` + `bdd` de la banda NO viven
  aquí — viven en `703_definition/` (output del paso *Definir*). Este carril es solo *Planear* (celda).
