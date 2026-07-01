"""generate_c1.py — Generador sintético del golden client C1 (fixture del Tracer Bullet).

Plano CONSTRUCCIÓN del MOTOR (D-001). Produce la FUENTE CRUDA de C1 (lo que un cliente entregaría),
NO la capa bronze: bronze nace en la celda 020_ingestion (ver C1_design.md §2). Determinista por
semilla fija (D-012): regenerar produce el mismo C1.

Diseño de referencia: 720_build/golden_client/C1_design.md
Decisiones: D-012 (golden client + snapshots), D-014 (grain producto×geo), D-015 (walking skeleton),
D-019 (financieros en bronze → van en la fuente), D-023 (Python).

Salida (en 720_build/golden_client/C1/):
  - source/demanda_historica.csv   → historia visible (train), fuente para 020_ingestion
  - source/demanda_holdout.csv     → hold-out de actuals, solo para 075_monitoring
  - generation_report.json         → semilla, parámetros y filas ensuciadas (auditable)

Uso:
  python generate_c1.py            # regenera C1 con los parámetros por defecto (semilla fija)

Nota: los nombres de columna de la fuente están EN ESPAÑOL a propósito — simulan "cómo los nombra el
cliente"; 015_onboarding los mapea al esquema canónico (esa es su razón de ser).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

# --- Rutas (relativas a este archivo, robustas al cwd) ---------------------------------------
HERE = Path(__file__).resolve().parent
C1_DIR = HERE.parent / "C1"
SOURCE_DIR = C1_DIR / "source"
REPORT_PATH = C1_DIR / "generation_report.json"


# --- Parámetros del generador (D-014). C1 = esquina mínima. -----------------------------------
@dataclass
class C1Params:
    semilla: int = 42
    # Tiempo
    inicio: date = date(2023, 1, 1)     # primer período (mensual)
    n_periodos: int = 36                # longitud total de la historia
    hold_out_k: int = 6                 # últimos K períodos reservados para Monitoring (075)
    # Grain producto (jerarquía superficial en C1: 1 familia/categoría/subcategoría, N SKU)
    familia: str = "Bebidas"
    categoria: str = "Bebidas no alcohólicas"
    subcategoria: str = "Gaseosas"
    # Grain geografía (1 región/país/ciudad/sede)
    region: str = "Andina"
    pais: str = "Colombia"
    ciudad: str = "Bogotá"
    sede: str = "CD Bogotá Norte"
    # Modelo de demanda
    sigma_ruido: float = 0.10           # dispersión relativa del ruido gaussiano
    # Estacionalidad mensual (factor multiplicativo por mes 1..12): pico en diciembre, valle en enero/febrero.
    # Sostiene la hipótesis testeable "la demanda sube en diciembre" (business_hypothesis → 040_exploration).
    estacionalidad: tuple = (0.85, 0.88, 0.95, 1.00, 1.02, 1.00,
                             0.98, 1.00, 1.05, 1.10, 1.20, 1.45)
    # Ruido de calidad (para que 030_cleaning tenga trabajo real, C1_design §6)
    pct_nulos: float = 0.02             # ~2% de cantidad_demandada a NULL
    n_duplicados: int = 4               # nº de filas duplicadas exactas a inyectar


# Catálogo de SKUs de C1 (7 series). base=nivel medio de demanda; trend=pendiente anual relativa;
# precio > costo (margen positivo para 070_reporting). costo_inv = holding por unidad/período.
SKUS: list[dict] = [
    # sku,      nombre,                     base, trend,  precio, costo, costo_inv
    ("SKU-001", "Gaseosa Cola 350ml",       1800, 0.06,   2500,  1500,   40),
    ("SKU-002", "Gaseosa Cola 1.5L",         950, 0.04,   5200,  3200,   90),
    ("SKU-003", "Gaseosa Naranja 350ml",     700, 0.02,   2400,  1450,   38),
    ("SKU-004", "Gaseosa Naranja 1.5L",      420, 0.03,   5000,  3100,   88),
    ("SKU-005", "Gaseosa Limón 350ml",       520, -0.02,  2400,  1450,   38),
    ("SKU-006", "Agua con gas 500ml",        1150, 0.08,   1800,  1000,   30),
    ("SKU-007", "Gaseosa Uva 350ml",         260, 0.01,   2450,  1480,   39),
]


def _month_starts(inicio: date, n: int) -> list[date]:
    """Devuelve n primeros-de-mes consecutivos a partir de `inicio`."""
    periods = pd.date_range(start=pd.Timestamp(inicio), periods=n, freq="MS")
    return [p.date() for p in periods]


def _series_demanda(rng: np.random.Generator, base: float, trend: float,
                    estacionalidad: tuple, periodos: list[date], sigma: float) -> list[int]:
    """Genera la demanda de una serie: nivel + tendencia + estacionalidad mensual + ruido."""
    out = []
    n = len(periodos)
    for t, p in enumerate(periodos):
        factor_tendencia = 1.0 + trend * (t / 12.0)
        factor_estacional = estacionalidad[p.month - 1]
        ruido = rng.normal(0.0, sigma)
        valor = base * factor_tendencia * factor_estacional * (1.0 + ruido)
        out.append(max(0, int(round(valor))))
    return out


def generar(params: C1Params) -> dict:
    rng = np.random.default_rng(params.semilla)
    periodos = _month_starts(params.inicio, params.n_periodos)

    filas: list[dict] = []
    for sku, nombre, base, trend, precio, costo, costo_inv in SKUS:
        demanda = _series_demanda(rng, base, trend, params.estacionalidad, periodos, params.sigma_ruido)
        for p, q in zip(periodos, demanda):
            filas.append({
                "periodo": p.isoformat(),
                "familia": params.familia,
                "categoria": params.categoria,
                "subcategoria": params.subcategoria,
                "sku": sku,
                "nombre_producto": nombre,
                "region": params.region,
                "pais": params.pais,
                "ciudad": params.ciudad,
                "sede": params.sede,
                "cantidad_demandada": q,
                "precio_unitario_venta": precio,
                "costo_unitario_venta": costo,
                "costo_inventario": costo_inv,
            })

    df = pd.DataFrame(filas)

    # --- Split train (historia visible) / hold-out (actuals para Monitoring) -----------------
    corte = params.n_periodos - params.hold_out_k
    periodos_train = set(p.isoformat() for p in periodos[:corte])
    periodos_holdout = set(p.isoformat() for p in periodos[corte:])
    df_train = df[df["periodo"].isin(periodos_train)].copy().reset_index(drop=True)
    df_holdout = df[df["periodo"].isin(periodos_holdout)].copy().reset_index(drop=True)

    # --- Ruido de calidad SOLO sobre la historia visible (030_cleaning limpia bronze, no el hold-out) ---
    reporte_suciedad = _ensuciar(rng, df_train, params)

    # --- Escritura -----------------------------------------------------------------------------
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    ruta_hist = SOURCE_DIR / "demanda_historica.csv"
    ruta_hold = SOURCE_DIR / "demanda_holdout.csv"
    df_train.to_csv(ruta_hist, index=False, encoding="utf-8")
    df_holdout.to_csv(ruta_hold, index=False, encoding="utf-8")

    reporte = {
        "cliente": "C1",
        "descripcion": "Golden client mínimo (esquina C1 de la matriz 2x2, D-014). Fuente cruda, no bronze.",
        "semilla": params.semilla,
        "parametros": {
            **{k: (v.isoformat() if isinstance(v, date) else v) for k, v in asdict(params).items()},
        },
        "grain": {
            "producto": ["familia", "categoria", "subcategoria", "sku"],
            "geografia": ["region", "pais", "ciudad", "sede"],
            "periodicidad": "mensual",
            "n_series": len(SKUS),
            "series": [s[0] for s in SKUS],
        },
        "tiempo": {
            "primer_periodo": periodos[0].isoformat(),
            "ultimo_periodo": periodos[-1].isoformat(),
            "n_periodos_total": params.n_periodos,
            "n_periodos_train": corte,
            "hold_out_k": params.hold_out_k,
            "primer_periodo_holdout": periodos[corte].isoformat(),
        },
        "hipotesis_incrustada": (
            "La demanda sube en diciembre (factor estacional 1.45) y baja en enero/febrero; "
            "verificable aguas abajo en 040_exploration."
        ),
        "financieros_en_fuente": ["precio_unitario_venta", "costo_unitario_venta", "costo_inventario"],
        "ruido_calidad": reporte_suciedad,
        "salidas": {
            "historia": str(ruta_hist.relative_to(HERE.parent)),
            "holdout": str(ruta_hold.relative_to(HERE.parent)),
            "filas_historia": len(df_train),
            "filas_holdout": len(df_holdout),
        },
    }
    REPORT_PATH.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")
    return reporte


def _ensuciar(rng: np.random.Generator, df: pd.DataFrame, params: C1Params) -> dict:
    """Inyecta nulos y duplicados deterministas para que 030_cleaning tenga trabajo real (C1_design §6)."""
    n = len(df)
    # Nulos en cantidad_demandada
    n_nulos = int(round(n * params.pct_nulos))
    idx_nulos = sorted(rng.choice(n, size=n_nulos, replace=False).tolist())
    df.loc[idx_nulos, "cantidad_demandada"] = np.nan

    # Duplicados exactos: repetir n_duplicados filas al azar (append)
    idx_dup = sorted(rng.choice(n, size=params.n_duplicados, replace=False).tolist())
    dup_rows = df.loc[idx_dup].copy()
    df_dup = pd.concat([df, dup_rows], ignore_index=True)
    # Reasignar in-place el contenido ensuciado con duplicados
    df.drop(df.index, inplace=True)
    for col in df_dup.columns:
        df[col] = df_dup[col].values

    return {
        "nulos_en_cantidad_demandada": n_nulos,
        "indices_nulos": idx_nulos,
        "duplicados_inyectados": params.n_duplicados,
        "indices_duplicados_origen": idx_dup,
        "nota": "Poco a propósito (E4): lo justo para ejercitar 030_cleaning L0. Solo en la historia visible.",
    }


if __name__ == "__main__":
    rep = generar(C1Params())
    print("Golden client C1 generado.")
    print(f"  historia: {rep['salidas']['filas_historia']} filas -> {rep['salidas']['historia']}")
    print(f"  holdout : {rep['salidas']['filas_holdout']} filas -> {rep['salidas']['holdout']}")
    print(f"  series  : {rep['grain']['n_series']}  |  semilla: {rep['semilla']}")
    print(f"  nulos   : {rep['ruido_calidad']['nulos_en_cantidad_demandada']}  |  "
          f"duplicados: {rep['ruido_calidad']['duplicados_inyectados']}")
    print(f"  reporte : {REPORT_PATH.relative_to(HERE.parent)}")
