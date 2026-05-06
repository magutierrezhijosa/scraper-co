###### EXTRACTOR -- Analizar HTML y extraer los datos
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from config import (
    BASE_URL,
    SELECTOR_PUBLICACIONES,
    PAGINAS_EXCLUIDAS,
    PATRONES_CONTENIDO,
    MAX_PROFUNDIDAD,
    MAX_ENLACES_INTERNOS,
    logger
)


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
            url_completa = BASE_URL + href

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
            url_pdf = href if href.startswith("http") else BASE_URL + href
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

        url_completa = BASE_URL + href
        if url_completa not in enlaces:
            enlaces.append(url_completa)

    return enlaces


def buscar_pdfs_recursivo(
    pagina: Page,
    url: str,
    titulo_publicacion: str,
    profundidad: int = 0,
    urls_ya_guardadas: Optional[set] = None
) -> List[Dict[str, str]]:
    """
    Busca PDFs en una página recursivamente.
    Si no encuentra PDFs, explora enlaces internos.
    La profundidad evita bucles infinitos.
    """
    if urls_ya_guardadas is None:
        urls_ya_guardadas = set()

    if profundidad > MAX_PROFUNDIDAD:
        return []

    if not titulo_publicacion or not titulo_publicacion.strip():
        return []

    logger.info(f"{'  ' * profundidad}Buscando PDFs en: {url[:60]}")

    resultados: List[Dict[str, str]] = []

    try:
        pagina.goto(url, timeout=30000)
        pagina.wait_for_load_state("networkidle", timeout=30000)

        from navegador import click_ver_mais
        click_ver_mais(pagina)

        pdfs = extraer_pdfs(pagina)

        if pdfs:
            logger.info(f"{'  ' * profundidad}{len(pdfs)} PDF(s) encontrados")
            for pdf in pdfs:
                if pdf["url_pdf"] not in urls_ya_guardadas:
                    resultados.append({
                        "titulo_publicacion": titulo_publicacion,
                        "titulo_pdf": pdf["titulo_publicacion"],
                        "url_pdf": pdf["url_pdf"]
                    })
                    urls_ya_guardadas.add(pdf["url_pdf"])
        else:
            enlaces = extraer_enlaces_internos(pagina)
            logger.info(f"{'  ' * profundidad}Sin PDFs, explorando {len(enlaces)} enlaces internos...")
            for enlace in enlaces[:MAX_ENLACES_INTERNOS]:
                sub_resultados = buscar_pdfs_recursivo(
                    pagina,
                    enlace,
                    titulo_publicacion,
                    profundidad + 1,
                    urls_ya_guardadas
                )
                resultados.extend(sub_resultados)

    except Exception as e:
        logger.error(f"Error al procesar {url}: {e}")

    return resultados