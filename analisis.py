"""Análisis reproducible de comentarios sobre movilidad. Datos de demostración, no observaciones reales."""
from collections import Counter
import csv
import re
import unicodedata
from pathlib import Path

LUGARES = ['Portal Norte', 'Portal Suba', 'Portal Américas', 'Portal Usme', 'Calle 80', 'Ricaurte']
PROBLEMAS = {
    'demora': ('demora', 'demoras', 'tarda', 'espera', 'retraso', 'retrasos'),
    'aglomeración': ('lleno', 'llena', 'aglomeracion', 'aglomeraciones', 'hacinamiento'),
    'seguridad': ('inseguridad', 'robo', 'robos', 'inseguro'),
    'información': ('informacion', 'avisos', 'senalizacion', 'no informan'),
    'accesibilidad': ('accesibilidad', 'rampa', 'silla de ruedas', 'ascensor'),
}
RECOMENDACIONES = {
    'demora': 'Evaluar intervalos de despacho y regularidad de la ruta en las horas reportadas.',
    'aglomeración': 'Contrastar reportes de ocupación con aforos antes de redistribuir flota.',
    'seguridad': 'Coordinar revisión de incidentes con personal operativo y autoridades.',
    'información': 'Revisar avisos de servicio y canales de información al usuario.',
    'accesibilidad': 'Verificar condiciones de acceso y reportar barreras a la entidad competente.',
}

def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto).lower()) if unicodedata.category(c) != 'Mn')

def cargar_modelo():
    try:
        import spacy
        return spacy.load('es_core_news_sm')
    except (ImportError, OSError):
        return None

def analizar_comentarios(comentarios, nlp=None):
    """Usa spaCy para NER opcional y reglas auditables para categorizar."""
    resumen = Counter()
    pares = Counter()
    detalles = []
    for comentario in comentarios:
        original = str(comentario).strip()
        if not original:
            continue
        texto = normalizar(original)
        lugares = [lugar for lugar in LUGARES if normalizar(lugar) in texto]
        problemas = [categoria for categoria, claves in PROBLEMAS.items()
                     if any(re.search(r'(?<!\w)' + re.escape(clave) + r'(?!\w)', texto) for clave in claves)]
        entidades = []
        if nlp is not None:
            doc = nlp(original)
            entidades = [ent.text for ent in doc.ents if ent.label_ in ('LOC', 'GPE')]
        for problema in problemas:
            resumen[problema] += 1
            for lugar in lugares:
                pares[(lugar, problema)] += 1
        detalles.append({'texto': original, 'lugares': lugares, 'problemas': problemas, 'entidades_spacy': entidades})
    return {'total': len(detalles), 'categorias': dict(resumen), 'pares': dict(pares), 'detalles': detalles}

def proponer_optimizaciones(analisis, umbral=5):
    if umbral < 1:
        raise ValueError('El umbral debe ser positivo')
    propuestas = []
    for (lugar, problema), conteo in sorted(analisis['pares'].items(), key=lambda x: (-x[1], x[0])):
        if conteo >= umbral:
            propuestas.append({'lugar': lugar, 'problema': problema, 'menciones': conteo,
                               'propuesta': RECOMENDACIONES[problema], 'alcance': 'Hipótesis para verificar; no decisión operativa automática'})
    return propuestas

def leer_csv(ruta):
    with open(ruta, encoding='utf-8-sig', newline='') as archivo:
        lector = csv.DictReader(archivo)
        if not lector.fieldnames or 'texto' not in lector.fieldnames:
            raise ValueError('El CSV debe contener una columna llamada texto')
        return [fila['texto'] for fila in lector if fila.get('texto', '').strip()]

def escribir_resultados(analisis, propuestas, salida):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    with (salida / 'categorias.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['categoria', 'menciones']); w.writerows(sorted(analisis['categorias'].items()))
    with (salida / 'propuestas.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['lugar', 'problema', 'menciones', 'propuesta', 'alcance']); w.writeheader(); w.writerows(propuestas)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        datos = sorted(analisis['categorias'].items(), key=lambda x: x[1], reverse=True)
        if datos:
            fig, ax = plt.subplots(figsize=(8.2, 4.2))
            ax.bar([x[0] for x in datos], [x[1] for x in datos], color='#1761A0')
            ax.set_ylabel('Menciones clasificadas')
            ax.set_title('Problemas en comentarios de demostración (no datos reales)')
            ax.tick_params(axis='x', rotation=15)
            fig.tight_layout(); fig.savefig(salida / 'grafico_categorias.png', dpi=170); plt.close(fig)
    except ImportError:
        print('matplotlib no está instalado: se omitió el gráfico.')
