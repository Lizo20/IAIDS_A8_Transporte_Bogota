"""Punto de entrada para el estudio de caso."""
import argparse
from pathlib import Path
from analisis import analizar_comentarios, cargar_modelo, leer_csv, proponer_optimizaciones, escribir_resultados
from recoleccion_selenium import recolectar, guardar

def main():
    parser = argparse.ArgumentParser(description='Análisis textual de transporte público de Bogotá')
    parser.add_argument('--csv', default='datos/comentarios_demo.csv')
    parser.add_argument('--url', help='URL pública autorizada para extracción experimental')
    parser.add_argument('--selector', default='article')
    parser.add_argument('--umbral', type=int, default=5)
    argumentos = parser.parse_args()
    if argumentos.url:
        textos = recolectar(argumentos.url, argumentos.selector)
        if not textos:
            raise SystemExit('Sin textos accesibles; no se sustituirán por supuestos datos reales.')
        Path('datos').mkdir(exist_ok=True); guardar(textos, 'datos/comentarios_recolectados.csv')
        print('Extracción experimental guardada en datos/comentarios_recolectados.csv')
    else:
        textos = leer_csv(argumentos.csv)
        print('MODO DEMOSTRACIÓN: comentarios sintéticos, no publicados en redes sociales.')
    modelo = cargar_modelo()
    print('spaCy español:', 'activo' if modelo else 'no disponible (análisis por reglas)')
    analisis = analizar_comentarios(textos, modelo)
    propuestas = proponer_optimizaciones(analisis, argumentos.umbral)
    escribir_resultados(analisis, propuestas, 'resultados')
    print('Comentarios:', analisis['total']); print('Categorías:', analisis['categorias'])
    print('Propuestas sujetas a verificación:', len(propuestas))
    for item in propuestas: print(f"- {item['lugar']} / {item['problema']}: {item['menciones']} -> {item['propuesta']}")
    print('Archivos guardados en resultados/')

if __name__ == '__main__':
    main()
