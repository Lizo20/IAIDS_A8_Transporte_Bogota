"""Validación unitaria y basada en propiedades: no depende de internet."""
import pytest
from hypothesis import given, strategies as st
from analisis import analizar_comentarios, proponer_optimizaciones, normalizar

def test_detecta_demoras_por_lugar():
    analisis = analizar_comentarios(['En Portal Norte la espera es larga', 'Portal Norte tiene demora'])
    assert analisis['pares'][('Portal Norte', 'demora')] == 2

def test_umbral_inclusivo():
    resultado = analizar_comentarios(['Portal Suba demora'] * 5)
    assert len(proponer_optimizaciones(resultado, 5)) == 1
    assert not proponer_optimizaciones(resultado, 6)

def test_sin_comentarios():
    resultado = analizar_comentarios([])
    assert resultado['total'] == 0 and not proponer_optimizaciones(resultado)

def test_umbral_invalido():
    with pytest.raises(ValueError): proponer_optimizaciones(analizar_comentarios([]), 0)

@given(st.lists(st.text(max_size=90), max_size=25))
def test_propiedad_conteos_no_negativos(textos):
    resultado = analizar_comentarios(textos)
    assert 0 <= resultado['total'] <= len(textos)
    assert all(v >= 0 for v in resultado['categorias'].values())
    assert isinstance(proponer_optimizaciones(resultado), list)

@given(st.text(max_size=100))
def test_propiedad_normalizacion_idempotente(texto):
    assert normalizar(normalizar(texto)) == normalizar(texto)
