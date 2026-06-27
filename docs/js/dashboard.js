const RUTA_DATOS = "data/datos_dashboard.json";

function formatearValor(valor, unidad) {
    if (valor === null || valor === undefined) {
        return "No disponible";
    }

    return `${valor} ${unidad}`;
}

function mostrarEncabezado(data) {
    document.getElementById("titulo").textContent = data.titulo;
    document.getElementById("descripcion").textContent = data.descripcion;
    document.getElementById("fuente").textContent = `Fuente: ${data.fuente}`;

    document.getElementById("periodo").textContent =
        `${data.periodo.inicio} hasta ${data.periodo.fin}`;
}

function mostrarTarjetas(data) {
    const contenedor = document.getElementById("tarjetas");
    contenedor.innerHTML = "";

    Object.values(data.metricas).forEach(metrica => {
        const tarjeta = document.createElement("div");
        tarjeta.classList.add("tarjeta");

        tarjeta.innerHTML = `
            <h3>${metrica.nombre}</h3>
            <p class="valor-principal">${formatearValor(metrica.ultimo_valor, metrica.unidad)}</p>
            <p class="detalle">Último dato: ${metrica.fecha_ultimo_valor}</p>
            <p class="detalle">Máximo: ${formatearValor(metrica.maximo, metrica.unidad)} en ${metrica.fecha_maximo}</p>
            <p class="detalle">Mínimo: ${formatearValor(metrica.minimo, metrica.unidad)} en ${metrica.fecha_minimo}</p>
            <p class="detalle">Promedio: ${formatearValor(metrica.promedio, metrica.unidad)}</p>
        `;

        contenedor.appendChild(tarjeta);
    });
}

function mostrarConclusiones(data) {
    const contenedor = document.getElementById("conclusiones");
    contenedor.innerHTML = "";

    data.conclusiones.forEach(conclusion => {
        const parrafo = document.createElement("p");
        parrafo.textContent = conclusion;
        contenedor.appendChild(parrafo);
    });
}

function mostrarTabla(data) {
    const cuerpoTabla = document.getElementById("tabla-datos");
    cuerpoTabla.innerHTML = "";

    const ultimosDatos = data.tabla.slice(-10).reverse();

    ultimosDatos.forEach(fila => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${fila.fecha}</td>
            <td>${fila.inflacion_12_meses ?? ""}</td>
            <td>${fila.tipo_cambio_promedio ?? ""}</td>
            <td>${fila.tasa_referencia ?? ""}</td>
        `;

        cuerpoTabla.appendChild(tr);
    });
}

function obtenerSerie(data, idSerie) {
    return data.series.find(serie => serie.id === idSerie);
}

function crearGraficoLinea(idCanvas, serie, tituloEjeY) {
    const contexto = document.getElementById(idCanvas);

    const etiquetas = serie.datos.map(dato => dato.fecha);
    const valores = serie.datos.map(dato => dato.valor);

    new Chart(contexto, {
        type: "line",
        data: {
            labels: etiquetas,
            datasets: [
                {
                    label: serie.nombre,
                    data: valores,
                    tension: 0.25,
                    pointRadius: 2,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    mode: "index",
                    intersect: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxTicksLimit: 12
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: tituloEjeY
                    }
                }
            }
        }
    });
}

function mostrarGraficos(data) {
    const serieInflacion = obtenerSerie(data, "inflacion_12_meses");
    const serieTipoCambio = obtenerSerie(data, "tipo_cambio_promedio");
    const serieTasaReferencia = obtenerSerie(data, "tasa_referencia");

    crearGraficoLinea("graficoInflacion", serieInflacion, "%");
    crearGraficoLinea("graficoTipoCambio", serieTipoCambio, "S/ por US$");
    crearGraficoLinea("graficoTasaReferencia", serieTasaReferencia, "%");
}

function crearGraficoComparativo(data) {
    const serieInflacion = obtenerSerie(data, "inflacion_12_meses");
    const serieTasaReferencia = obtenerSerie(data, "tasa_referencia");

    const mapaInflacion = new Map(
        serieInflacion.datos.map(dato => [dato.fecha, dato.valor])
    );

    const mapaTasa = new Map(
        serieTasaReferencia.datos.map(dato => [dato.fecha, dato.valor])
    );

    const fechas = Array.from(
        new Set([
            ...serieInflacion.datos.map(dato => dato.fecha),
            ...serieTasaReferencia.datos.map(dato => dato.fecha)
        ])
    ).sort();

    const valoresInflacion = fechas.map(fecha =>
        mapaInflacion.has(fecha) ? mapaInflacion.get(fecha) : null
    );

    const valoresTasa = fechas.map(fecha =>
        mapaTasa.has(fecha) ? mapaTasa.get(fecha) : null
    );

    const contexto = document.getElementById("graficoComparativo");

    new Chart(contexto, {
        type: "line",
        data: {
            labels: fechas,
            datasets: [
                {
                    label: "Inflación 12 meses",
                    data: valoresInflacion,
                    tension: 0.25,
                    pointRadius: 2,
                    borderWidth: 2
                },
                {
                    label: "Tasa de referencia BCRP",
                    data: valoresTasa,
                    tension: 0.25,
                    pointRadius: 2,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    mode: "index",
                    intersect: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxTicksLimit: 12
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "%"
                    }
                }
            }
        }
    });
}


async function cargarDashboard() {
    try {
        const respuesta = await fetch(RUTA_DATOS);

        if (!respuesta.ok) {
            throw new Error("No se pudo cargar el archivo JSON");
        }

        const data = await respuesta.json();

        mostrarEncabezado(data);
        mostrarTarjetas(data);
        mostrarGraficos(data);
        crearGraficoComparativo(data);
        mostrarConclusiones(data);
        mostrarTabla(data);
        
        console.log("Dashboard cargado correctamente", data);

    } catch (error) {
        console.error(error);
        document.getElementById("descripcion").textContent =
            "Error al cargar los datos del dashboard.";
    }
}

cargarDashboard();