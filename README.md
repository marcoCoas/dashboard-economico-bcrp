\# Dashboard económico del Perú - BCRP



Proyecto de análisis de datos económicos del Perú usando datos abiertos del Banco Central de Reserva del Perú (BCRP).



El objetivo es descargar, limpiar, analizar y visualizar indicadores económicos en una página web.



\## Indicadores analizados



\* Inflación 12 meses

\* Tipo de cambio promedio mensual

\* Tasa de referencia del BCRP



\## Tecnologías utilizadas



\* Python

\* Pandas

\* Requests

\* HTML

\* CSS

\* JavaScript

\* Chart.js

\* GitHub Pages



\## Estructura del proyecto



```text

dashboard-economico-bcrp/

│

├── src/          # Scripts Python para descarga, limpieza y análisis

├── data/         # Datos generados para el dashboard

├── web/          # Versión de desarrollo de la página

├── docs/         # Versión publicada con GitHub Pages

├── requirements.txt

└── README.md

```



\## Flujo del proyecto



```text

BCRP API

&#x20;  ↓

Python

&#x20;  ↓

JSON procesado

&#x20;  ↓

Dashboard web

```



\## Cómo ejecutar localmente



Clonar el repositorio:



```bash

git clone https://github.com/marcoCoas/dashboard-economico-bcrp.git

cd dashboard-economico-bcrp

```



Crear entorno virtual e instalar dependencias:



```cmd

python -m venv .venv

.venv\\Scripts\\activate

pip install -r requirements.txt

```



Ejecutar los scripts de datos:



```cmd

python src\\descargar\_bcrp.py

python src\\limpiar\_datos.py

python src\\analizar\_datos.py

python src\\generar\_json.py

```



Copiar el JSON generado a la carpeta pública:



```cmd

copy data\\output\\datos\_dashboard.json docs\\data\\datos\_dashboard.json

```



Levantar servidor local:



```cmd

python -m http.server 8000

```



Abrir en el navegador:



```text

http://localhost:8000/docs/

```



\## Publicación



El proyecto está preparado para publicarse con GitHub Pages desde la carpeta `/docs`.



Configuración:



```text

Settings → Pages → Deploy from a branch → master → /docs

```



\## Resultados



El dashboard muestra:



\* Tarjetas resumen

\* Gráficos de evolución

\* Tabla con los últimos datos

\* Conclusiones descriptivas



\## Limitaciones



Este proyecto realiza un análisis descriptivo. Las conclusiones muestran tendencias y variaciones, pero no prueban causalidad entre variables económicas.



\## Estado



Proyecto en desarrollo.



