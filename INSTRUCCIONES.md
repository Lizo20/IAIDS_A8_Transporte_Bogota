# Guía de ejecución y entrega — IAIDS_A8

## 1. Preparación
Instale Python 3.11/3.12 y Google Chrome. En PowerShell, dentro de la carpeta del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

Si PowerShell bloquea la activación, ejecute directamente `.venv\Scripts\python.exe` en lugar de `python`. Selenium Manager normalmente configura ChromeDriver sin descarga manual.

## 2. Análisis de demostración
```powershell
python main.py
python main.py --umbral 8
```

Entrada: `datos/comentarios_demo.csv` contiene 65 comentarios **inventados**. Salidas: `resultados/categorias.csv`, `resultados/propuestas.csv` y `resultados/grafico_categorias.png`.

## 3. Pruebas
```powershell
python -m pytest -v test_analisis.py
```

Las pruebas de Hypothesis generan entradas variadas automáticamente. Guarde una captura de la consola con el resultado real. No declare que las pruebas se aprobaron hasta ejecutarlas.

## 4. Selenium (experimental)
```powershell
python main.py --url "https://SITIO-PUBLICO-AUTORIZADO" --selector "article"
```

El sitio debe permitir la extracción, no depender de autenticación ni impedirla mediante sus controles. X/Twitter puede bloquear Selenium. No se simulan publicaciones reales cuando una extracción falla. También puede usar `python main.py --csv datos/archivo_propiedad.csv` con un CSV legítimamente obtenido que incluya la columna `texto`.

## 5. Entrega de UNIMINUTO
Abra el informe Word incluido en el paquete ZIP original, complete los datos personales y añada la URL del repositorio:

https://github.com/Lizo20/IAIDS_A8_Transporte_Bogota

Incluya capturas de `python main.py`, `python -m pytest -v test_analisis.py` y el gráfico generado. El informe exige Arial 11, interlineado 1.5 y 8 a 12 páginas de desarrollo, sin portada ni bibliografía.

## 6. Alcance
El análisis clasifica por reglas lingüísticas y utiliza spaCy opcionalmente para reconocimiento de entidades; no entrena un modelo supervisado. Las 6 recomendaciones derivadas de los datos de demostración son hipótesis para validación con fuentes operativas y usuarios.
