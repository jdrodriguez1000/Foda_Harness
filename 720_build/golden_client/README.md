# golden_client — Cliente de prueba canónico C1 + snapshots

> Infraestructura de construcción del MOTOR para probar la tubería **sin re-ejecutar toda la cadena**
> en cada celda (`D-012` híbrido). Carril compartido entre bandas. Plano CONSTRUCCIÓN (`D-001`): nada
> de aquí viaja a una instancia. Diseño completo en **`C1_design.md`**.

## Estructura

```
golden_client/
├── C1_design.md              ← diseño del golden client C1 (aprobado; leer primero)
├── docker-compose.yml        ← Postgres local desechable (postgres:17-alpine, puerto host 55432)
├── .env.example              ← plantilla de credenciales (COMMITEADA)
├── .env                      ← credenciales reales (GITIGNORED)
├── db/init/                  ← scripts SQL de init (crean el schema golden_client)
├── generator/
│   └── generate_c1.py        ← generador sintético parametrizado (D-014), determinista (semilla fija)
├── C1/
│   ├── questionnaires/       ← cuestionarios pre-respondidos (insumo de 010_discovery L0)
│   ├── source/               ← FUENTE CRUDA de C1 (GITIGNORED, regenerable): lo que "entrega el cliente"
│   │   ├── demanda_historica.csv   → historia visible (train) → la lee 020_ingestion
│   │   └── demanda_holdout.csv     → hold-out de actuals → solo 075_monitoring
│   └── generation_report.json ← semilla, parámetros, filas ensuciadas (auditable, COMMITEADO)
└── snapshots/                ← congelado bronze/silver/gold + artefactos por celda (D-012)
```

> **Frontera del generador (decisión):** produce la **fuente cruda** (CSV), **no** bronze. Bronze nace en
> la celda `020_ingestion` y se congela en `snapshots/`. Ver `C1_design.md` §2.

## C1 en breve
- **Grain (`D-014`, esquina mínima):** 1 familia/categoría/subcategoría × ~7 SKUs · 1 región/país/ciudad/sede · **mensual** · 36 meses → **~7 series**.
- **Patrón incrustado:** pico de demanda en **diciembre** (hipótesis testeable para `040_exploration`).
- **Ruido de calidad:** pocos nulos + duplicados (trabajo real para `030_cleaning`).
- **Hold-out:** últimos **6** meses reservados como actuals para `075_monitoring`.
- **Financieros en la fuente:** precio/costo unitario + costo de inventario (los lee `070_reporting` desde bronze, `D-019`).

## Uso

**1) Levantar el Postgres local (una vez):**
```powershell
cd 720_build/golden_client
copy .env.example .env   # y ajustar POSTGRES_PASSWORD
docker compose up -d     # postgres:17-alpine en localhost:55432, DB foda, schema golden_client
```
Reset total del fixture: `docker compose down -v` (borra el volumen).

**2) (Re)generar la fuente cruda de C1:**
```powershell
python generator/generate_c1.py
```
Determinista: misma semilla → mismo C1 (bytes equivalentes).

## Notas
- Aprovecha la **inmutabilidad** bronze → silver → gold (`D-012`).
- Fixtures escalonados (`D-014`): **C1 primario ya**; C4 (estrés) y C2/C3 bajo demanda (el generador ya queda parametrizado para instanciarlos).
- **Tarea `T-014`** (esta infraestructura) — prerrequisito de la primera celda (`010_discovery`) del Tracer Bullet.
- Los CSV de `source/` están **gitignored** (regenerables); lo versionado es el **generador** + `generation_report.json`.
