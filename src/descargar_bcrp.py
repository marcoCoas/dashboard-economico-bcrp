from pathlib import Path
import json
import requests


# Carpeta donde guardaremos los datos originales descargados del BCRP
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# Periodo inicial y final del análisis
# Usamos datos mensuales desde enero 2018 hasta mayo 2026
PERIODO_INICIO = "2018-1"
PERIODO_FIN = "2026-5"


SERIES_BCRP = {
    "inflacion_12_meses": {
        "codigo": "PN01273PM",
        "nombre": "Inflación 12 meses"
    },
    "tipo_cambio_promedio": {
        "codigo": "PN01246PM",
        "nombre": "Tipo de cambio promedio mensual"
    },
    "tasa_referencia": {
        "codigo": "PD04722MM",
        "nombre": "Tasa de referencia BCRP"
    }
}


def construir_url(codigo):
    return (
        f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
        f"{codigo}/json/{PERIODO_INICIO}/{PERIODO_FIN}/esp"
    )


def descargar_serie(nombre_archivo, codigo, nombre_serie):
    url = construir_url(codigo)

    print(f"Descargando: {nombre_serie}")
    print(f"URL: {url}")

    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()

    datos = respuesta.json()

    archivo_salida = RAW_DIR / f"{nombre_archivo}.json"

    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print(f"Guardado en: {archivo_salida}")
    print("-" * 60)


def main():
    for nombre_archivo, info in SERIES_BCRP.items():
        descargar_serie(
            nombre_archivo=nombre_archivo,
            codigo=info["codigo"],
            nombre_serie=info["nombre"]
        )

    print("Descarga completada correctamente.")


if __name__ == "__main__":
    main()