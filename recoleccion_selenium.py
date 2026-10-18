"""Recolector experimental de textos visibles en páginas públicas permitidas.
No evade autenticación, robots.txt, CAPTCHAs ni controles anti-bots.
"""
import csv
from urllib.parse import urlparse

def recolectar(url, selector='article', max_elementos=40):
    if urlparse(url).scheme not in ('http', 'https'):
        raise ValueError('Solo se permiten URLs HTTP o HTTPS')
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    opciones = Options(); opciones.add_argument('--headless=new'); opciones.add_argument('--window-size=1280,900')
    navegador = webdriver.Chrome(options=opciones)
    try:
        navegador.get(url)
        WebDriverWait(navegador, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        textos = [e.text.strip() for e in navegador.find_elements(By.CSS_SELECTOR, selector)]
        return list(dict.fromkeys(t for t in textos if t))[:max_elementos]
    finally:
        navegador.quit()

def guardar(textos, ruta):
    with open(ruta, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f); writer.writerow(['texto']); writer.writerows([[t] for t in textos])
