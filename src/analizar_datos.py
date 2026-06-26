from pathlib import Path
import json
import pandas as pd


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


ARCHIVO_DATOS = PROCESSED_DIR / "datos_economicos_limpios.csv"


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


def redondear(valor, decimales=2):
    if pd.isna(valor):
        return None
    return round(float(valor), decimales)


def calcular_metricas(df, columna):
    datos = df[["fecha", columna]].dropna().copy()

    if datos.empty:
        return None

    datos["variacion_mensual"] = datos[columna].diff()

    primer_registro = datos.iloc[0]
    ultimo_registro = datos.iloc[-1]

    maximo = datos.loc[datos[columna].idxmax()]
    minimo = datos.loc[datos[columna].idxmin()]

    mayor_subida = datos.loc[datos["variacion_mensual"].idxmax()]
    mayor_caida = datos.loc[datos["variacion_mensual"].idxmin()]

    valor_inicial = primer_registro[columna]
    valor_final = ultimo_registro[columna]

    variacion_absoluta = valor_final - valor_inicial

    if valor_inicial != 0:
        variacion_porcentual = (variacion_absoluta / valor_inicial) * 100
    else:
        variacion_porcentual = None

    metricas = {
        "fecha_inicio": str(primer_registro["fecha"]),
        "valor_inicio": redondear(valor_inicial),

        "fecha_fin": str(ultimo_registro["fecha"]),
        "valor_final": redondear(valor_final),

        "ultimo_valor": redondear(valor_final),
        "fecha_ultimo_valor": str(ultimo_registro["fecha"]),

        "maximo": redondear(maximo[columna]),
        "fecha_maximo": str(maximo["fecha"]),

        "minimo": redondear(minimo[columna]),
        "fecha_minimo": str(minimo["fecha"]),

        "promedio": redondear(datos[columna].mean()),

        "variacion_absoluta": redondear(variacion_absoluta),
        "variacion_porcentual": redondear(variacion_porcentual),

        "mayor_subida": redondear(mayor_subida["variacion_mensual"]),
        "fecha_mayor_subida": str(mayor_subida["fecha"]),

        "mayor_caida": redondear(mayor_caida["variacion_mensual"]),
        "fecha_mayor_caida": str(mayor_caida["fecha"])
    }

    return metricas


def generar_conclusion(nombre_variable, unidad, metricas):
    return (
        f"{nombre_variable}: entre {metricas['fecha_inicio']} y {metricas['fecha_fin']}, "
        f"el valor pasó de {metricas['valor_inicio']} {unidad} a "
        f"{metricas['valor_final']} {unidad}. "
        f"El máximo del periodo fue {metricas['maximo']} {unidad} en "
        f"{metricas['fecha_maximo']}, mientras que el mínimo fue "
        f"{metricas['minimo']} {unidad} en {metricas['fecha_minimo']}."
    )


def main():
    df = pd.read_csv(ARCHIVO_DATOS)

    resultado = {
        "periodo": {
            "inicio": str(df["fecha"].min()),
            "fin": str(df["fecha"].max())
        },
        "metricas": {},
        "conclusiones": []
    }

    registros_resumen = []

    for columna, info in VARIABLES.items():
        print(f"Analizando: {info['nombre']}")

        metricas = calcular_metricas(df, columna)

        if metricas is None:
            print(f"No hay datos para {columna}")
            continue

        resultado["metricas"][columna] = {
            "nombre": info["nombre"],
            "unidad": info["unidad"],
            **metricas
        }

        conclusion = generar_conclusion(
            nombre_variable=info["nombre"],
            unidad=info["unidad"],
            metricas=metricas
        )

        resultado["conclusiones"].append(conclusion)

        registros_resumen.append({
            "variable": info["nombre"],
            "unidad": info["unidad"],
            **metricas
        })

    ruta_json = OUTPUT_DIR / "resumen_metricas.json"
    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, ensure_ascii=False, indent=4)

    ruta_csv = PROCESSED_DIR / "resumen_metricas.csv"
    pd.DataFrame(registros_resumen).to_csv(
        ruta_csv,
        index=False,
        encoding="utf-8-sig"
    )

    print("-" * 60)
    print("Análisis generado correctamente.")
    print(f"JSON: {ruta_json}")
    print(f"CSV: {ruta_csv}")
    print("-" * 60)

    for conclusion in resultado["conclusiones"]:
        print(conclusion)
        print()


if __name__ == "__main__":
    main()