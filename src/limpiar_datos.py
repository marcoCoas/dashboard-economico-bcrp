from pathlib import Path
import json
import pandas as pd
import re


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


ARCHIVOS_SERIES = {
    "inflacion_12_meses": "inflacion_12_meses",
    "tipo_cambio_promedio": "tipo_cambio_promedio",
    "tasa_referencia": "tasa_referencia"
}


MESES = {
    "Ene": "01",
    "Feb": "02",
    "Mar": "03",
    "Abr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Ago": "08",
    "Set": "09",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dic": "12"
}


def convertir_fecha_bcrp(nombre_periodo):
    """
    Convierte fechas del BCRP como 'Ene.2018' a '2018-01'.
    """
    nombre_periodo = nombre_periodo.strip()

    patron = r"([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\.?\s*(\d{4})"
    coincidencia = re.search(patron, nombre_periodo)

    if not coincidencia:
        raise ValueError(f"No se pudo convertir la fecha: {nombre_periodo}")

    mes_texto = coincidencia.group(1)
    anio = coincidencia.group(2)

    mes = MESES.get(mes_texto)

    if mes is None:
        raise ValueError(f"Mes no reconocido: {mes_texto}")

    return f"{anio}-{mes}"


def convertir_valor(valor):
    """
    Convierte valores del BCRP a número decimal.
    Maneja valores vacíos o no disponibles.
    """
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor in ["", "-", "n.d.", "N.D.", "nd", "ND"]:
        return None

    if "," in valor and "." not in valor:
        valor = valor.replace(",", ".")
    else:
        valor = valor.replace(",", "")

    return float(valor)


def leer_serie_bcrp(nombre_archivo, nombre_columna):
    ruta_archivo = RAW_DIR / f"{nombre_archivo}.json"

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos_json = json.load(archivo)

    periodos = datos_json.get("periods", [])

    registros = []

    for periodo in periodos:
        fecha_bcrp = periodo.get("name")
        valores = periodo.get("values", [])

        if not valores:
            continue

        fecha = convertir_fecha_bcrp(fecha_bcrp)
        valor = convertir_valor(valores[0])

        registros.append({
            "fecha": fecha,
            nombre_columna: valor
        })

    df = pd.DataFrame(registros)
    df = df.sort_values("fecha")

    return df


def main():
    dataframes = []

    for nombre_archivo, nombre_columna in ARCHIVOS_SERIES.items():
        print(f"Limpiando serie: {nombre_columna}")

        df = leer_serie_bcrp(nombre_archivo, nombre_columna)

        ruta_salida = PROCESSED_DIR / f"{nombre_columna}.csv"
        df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")

        print(f"Archivo limpio guardado en: {ruta_salida}")
        dataframes.append(df)

    df_final = dataframes[0]

    for df in dataframes[1:]:
        df_final = pd.merge(df_final, df, on="fecha", how="outer")

    df_final = df_final.sort_values("fecha")

    ruta_final = PROCESSED_DIR / "datos_economicos_limpios.csv"
    df_final.to_csv(ruta_final, index=False, encoding="utf-8-sig")

    print("-" * 60)
    print("Datos unidos correctamente.")
    print(f"Archivo final: {ruta_final}")
    print("-" * 60)
    print(df_final.head())
    print("-" * 60)
    print(df_final.tail())


if __name__ == "__main__":
    main()