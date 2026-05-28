###### EXTRACTOR -- Analizar HTML y extraer los datos
from typing import Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import Page

from config import BASE_URL, PAGINAS_EXCLUIDAS, PATRONES_CONTENIDO, SELECTOR_PUBLICACIONES, logger


def obtener_publicaciones(pagina: Page) -> List[Dict[str, str]]:
    """Extrae título y enlace de cada publicación de la página principal"""
    html = pagina.content()
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("span", class_="grelha-item")
    logger.info(f"Encontrados {len(items)} publicaciones")

    publicaciones: List[Dict[str, str]] = []
    for item in items:
        enlace = item.find("a", class_="grelha-item-titulo")
        if enlace:
            titulo = enlace.get_text(strip=True)
            href = enlace.get("href")
            if not href:
                continue
            url_completa = urljoin(BASE_URL, href)

            publicaciones.append({
                "titulo": titulo,
                "url": url_completa
            })

    return publicaciones


def extraer_pdfs(pagina: Page) -> List[Dict[str, str]]:
    """Busca todos los enlaces a PDFs en la página actual"""
    html = pagina.content()
    soup = BeautifulSoup(html, "html.parser")
    pdfs: List[Dict[str, str]] = []

    for enlace in soup.find_all("a", href=True):
        href = enlace.get("href")
        if href and href.lower().endswith(".pdf"):
            url_pdf = urljoin(BASE_URL, href)
            titulo_pdf = enlace.get_text(strip=True) or "PDF sin título"
            pdfs.append({
                "titulo_publicacion": titulo_pdf,
                "url_pdf": url_pdf
            })

    return pdfs


def extraer_enlaces_internos(pagina: Page) -> List[str]:
    """Busca enlaces internos que puedan llevar a subpáginas con PDFs"""
    html = pagina.content()
    soup = BeautifulSoup(html, "html.parser")
    enlaces: List[str] = []

    for enlace in soup.find_all("a", href=True):
        href = enlace.get("href")
        if not href or not href.startswith("/"):
            continue
        if href.lower().endswith(".pdf"):
            continue
        if any(href.startswith(excluida) for excluida in PAGINAS_EXCLUIDAS):
            continue
        if href == "/":
            continue
        if not any(patron in href for patron in PATRONES_CONTENIDO):
            continue

        url_completa = urljoin(BASE_URL, href)
        if url_completa not in enlaces:
            enlaces.append(url_completa)

    return enlaces


