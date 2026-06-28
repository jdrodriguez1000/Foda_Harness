# 720_build — Ejecutar · Probar · Verificar (output de los pasos finales)

> Carril donde se **construye, prueba y verifica** cada celda del ciclo de vertical slice (`D-021`).
> Es el plano del **MOTOR** (`foda-*`): definiciones canónicas reutilizables, no runtime de instancia.

## Estructura
```
720_build/
├── <banda>/<flujo>/            ← celda construida (flujo × banda)
│   ├── agents/                 ← definición(es) del agente que opera el flujo
│   ├── skills/                 ← skills/comandos del flujo
│   ├── schemas/                ← esquemas de los artefactos de entrada/salida
│   ├── contract/               ← contrato I/O del flujo (lo que consume/produce)
│   ├── deliverables/           ← artefactos canónicos que el flujo emite
│   └── evaluation/             ← pruebas y criterios de verificación (paso C, contexto fresco)
├── _transversal/               ← andamiaje transversal TR-1..TR-4 (D-020), compartido entre bandas
│   ├── TR-1/ TR-2/ TR-3/ TR-4/
└── golden_client/              ← cliente de prueba canónico C1 + snapshots por capa/artefacto (D-012/D-014)
    └── snapshots/
```

## Convenciones
- `<banda>` ∈ `tracer-bullet`, `stabilization`, `mvp`, `evolution`, `final` (`D-017`).
- `<flujo>` = nombre canónico (`010_discovery` … `075_monitoring`), ver `700_brief/000_general_process.md`.
- **`_transversal/` y `golden_client/` NO cuelgan de una banda**: son infraestructura compartida.
  Las transversales **evolucionan por banda** (D-020) pero su carril es único; el peldaño activo de
  cada TR por banda lo fija el `slice_contract` de esa banda. En el Tracer Bullet solo TR-1/TR-2 están
  activas (TR-3/TR-4 diferidas).

## Reglas
- **Quien ejecuta ≠ quien verifica** (`P1`, `P3`, `D-021 §5`): `evaluation/` se corre en contexto
  fresco; nunca autoaprobación.
- En el Tracer Bullet, Diseñar/Planear/Ejecutar pueden colapsar en una sesión (E4), pero **Verificar
  se mantiene independiente** (`D-020`).
- Referencia de estructura: `Caden_Harness/720_build/` (`L-006`).
