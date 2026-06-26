from pathlib import Path
import json
import pandas as pd


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


ARCHIVO_DATOS_LIMPIOS = PROCESSED_DIR / "datos_economicos_limpios.csv"
ARCHIVO_RESUMEN = OUTPUT_DIR / "resumen_metricas.json"
ARCHIVO_DASHBOARD = OUTPUT_DIR / "datos_dashboard.json"


VARIABLES = {
    "inflacion_12_meses": {
        "nombre": "Inflación 12 meses",
        "unidad": "%"
    },
    "tipo_cambio_promedio": {
        "nombre": "Tipo de cambio promedio mensual",
        "unidad": "S/ por US$"
    },
    "tasa_referencia": {
        "nombre": "Tasa de referencia BCRP",
        "unidad": "%"
    }
}


def convertir_numero(valor):
    """
    Convierte valores numéricos para que puedan guardarse bien en JSON.
    Si el valor está vacío, devuelve None.
    """
    if pd.isna(valor):
        return None

    return round(float(valor), 4)


def crear_series(df):
    series = []

    for columna, info in VARIABLES.items():
        datos_serie = []

        for _, fila in df.iterrows():
            valor = convertir_numero(fila[columna])

            if valor is not None:
                datos_serie.append({
                    "fecha": str(fila["fecha"]),
                    "valor": valor
                })

        series.append({
            "id": columna,
            "nombre": info["nombre"],
            "unidad": info["unidad"],
            "datos": datos_serie
        })

    return series


def crear_tabla(df):
    tabla = []

    for _, fila in df.iterrows():
        tabla.append({
            "fecha": str(fila["fecha"]),
            "inflacion_12_meses": convertir_numero(fila["inflacion_12_meses"]),
            "tipo_cambio_promedio": convertir_numero(fila["tipo_cambio_promedio"]),
            "tasa_referencia": convertir_numero(fila["tasa_referencia"])
        })

    return tabla


def main():
    df = pd.read_csv(ARCHIVO_DATOS_LIMPIOS)

    with open(ARCHIVO_RESUMEN, "r", encoding="utf-8") as archivo:
        resumen = json.load(archivo)

    datos_dashboard = {
        "titulo": "Dashboard económico del Perú",
        "fuente": "Banco Central de Reserva del Perú - BCRPData",
        "descripcion": (
            "Análisis de inflación, tipo de cambio promedio mensual "
            "y tasa de referencia del BCRP."
        ),
        "periodo": {
            "inicio": str(df["fecha"].min()),
            "fin": str(df["fecha"].max())
        },
        "series": crear_series(df),
        "metricas": resumen["metricas"],
        "conclusiones": resumen["conclusiones"],
        "tabla": crear_tabla(df)
    }

    with open(ARCHIVO_DASHBOARD, "w", encoding="utf-8") as archivo:
        json.dump(datos_dashboard, archivo, ensure_ascii=False, indent=4)

    print("JSON final generado correctamente.")
    print(f"Archivo creado: {ARCHIVO_DASHBOARD}")
    print("-" * 60)
    print(f"Periodo: {datos_dashboard['periodo']['inicio']} a {datos_dashboard['periodo']['fin']}")
    print(f"Cantidad de series: {len(datos_dashboard['series'])}")
    print(f"Filas en tabla: {len(datos_dashboard['tabla'])}")


if __name__ == "__main__":
    main()