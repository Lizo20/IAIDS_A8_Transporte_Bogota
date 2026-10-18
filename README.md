# IAIDS_A8 — Optimización del transporte público en Bogotá

Proyecto académico de inteligencia artificial para analizar comentarios sobre transporte público, identificar problemas recurrentes y generar **propuestas sujetas a verificación**, sin tomar decisiones de operación automáticamente.

> **Importante:** los 65 comentarios de `datos/comentarios_demo.csv` son **sintéticos**; no son publicaciones obtenidas de redes sociales ni evidencia de demanda real. La recolección con Selenium es experimental y no se ha validado contra X/Twitter.

## Tecnologías
- Python 3.11 o 3.12
- Selenium: recopilación experimental de textos públicamente accesibles
- spaCy: análisis de entidades de lugar si se instala el modelo español
- Reglas lingüísticas auditables para clasificar problemas
- PyTest y Hypothesis: pruebas unitarias y basadas en propiedades
- Matplotlib: gráficos

## Instalar en Windows
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

## Ejecución
```powershell
python main.py
python -m pytest -v test_analisis.py
```
Produce los CSV `resultados/categorias.csv`, `resultados/propuestas.csv` y el gráfico `resultados/grafico_categorias.png`. Con `--umbral 8` se modifica el mínimo de menciones para proponer revisión.

## Recolección opcional
```powershell
python main.py --url "https://SITIO-PUBLICO-AUTORIZADO" --selector "article"
```
Solo para sitios que permitan esta operación y dispongan de contenidos accesibles; respete los términos del servicio, la privacidad y las restricciones de automatización.

## Resultados del conjunto demostrativo
65 comentarios, de los cuales 25 mencionan demora, 12 aglomeración, 9 seguridad, 7 información y 6 accesibilidad. Las 6 propuestas son **hipótesis de revisión**, no conclusiones operativas válidas para la ciudad.

## Evidencias e informe
El informe académico Word y el gráfico precalculado se entregaron en el paquete ZIP de la actividad. El gráfico también se genera al ejecutar el programa. Para entrega universitaria, añada capturas reales de la consola y de las pruebas al informe, complete la portada e incorpore el enlace a este repositorio. Las pruebas formales PyTest/Hypothesis y la recolección Selenium están pendientes de verificación en el entorno del estudiante.

Consulte `INSTRUCCIONES.md` para la guía detallada.