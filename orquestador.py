############## ORQUESTADOR - Coordina navegación y extracción ###############

from typing import Dict, List, Optional

from playwright.sync_api import Page

from config import MAX_ENLACES_INTERNOS, MAX_PROFUNDIDAD, logger
from extractor import extraer_enlaces_internos, extraer_pdfs
from navegador import cargar_subpagina, click_ver_mais


def buscar_pdfs_recursivo(
    pagina: Page,
    url: str,
    titulo_publicacion: str,
    profundidad: int = 0,
    urls_ya_guardadas: Optional[set] = None,
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
        if not cargar_subpagina(pagina, url):
            return resultados

        click_ver_mais(pagina)

        pdfs = extraer_pdfs(pagina)

        if pdfs:
            logger.info(f"{'  ' * profundidad}{len(pdfs)} PDF(s) encontrados")
            for pdf in pdfs:
                if pdf["url_pdf"] not in urls_ya_guardadas:
                    resultados.append(
                        {
                            "titulo_publicacion": titulo_publicacion,
                            "titulo_pdf": pdf["titulo_publicacion"],
                            "url_pdf": pdf["url_pdf"],
                        }
                    )
                    urls_ya_guardadas.add(pdf["url_pdf"])
        else:
            enlaces = extraer_enlaces_internos(pagina)
            logger.info(
                f"{'  ' * profundidad}Sin PDFs, explorando {len(enlaces)} enlaces internos..."
            )
            for enlace in enlaces[:MAX_ENLACES_INTERNOS]:
                sub_resultados = buscar_pdfs_recursivo(
                    pagina,
                    enlace,
                    titulo_publicacion,
                    profundidad + 1,
                    urls_ya_guardadas,
                )
                resultados.extend(sub_resultados)

    except Exception as e:
        logger.error(f"Error al procesar {url}: {e}")

    return resultados
