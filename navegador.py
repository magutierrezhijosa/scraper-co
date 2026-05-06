############# NAVEGADOR - Funciones relacionadas con Playwright

import time
from typing import Tuple, Optional

from playwright.sync_api import sync_playwright, Browser, Page, Playwright
from config import (
    URL_DESTAQUES,
    SELECTOR_PUBLICACIONES,
    HEADLESS,
    TIMEOUT_NAVEGAR,
    TIMEOUT_LOAD_STATE,
    MAX_REINTENTOS,
    REINTENTO_ESPERA,
    logger
)

def crear_navegador() -> Tuple[Playwright, Browser, Page]:
    """Inicia Playwright y devuelve el navegador y la página"""
    playwright = sync_playwright().start()
    navegador = playwright.chromium.launch(headless=HEADLESS)
    pagina = navegador.new_page()
    return playwright, navegador, pagina


def cerrar_navegador(playwright: Playwright, navegador: Browser) -> None:
    """Cierra el navegador y Playwright correctamente"""
    try:
        navegador.close()
        playwright.stop()
    except Exception as e:
        logger.error(f"Error al cerrar el navegador: {e}")


def _navegar_con_reintentos(pagina: Page, url: str) -> bool:
    """Navega a una URL con reintentos automáticos"""
    for intento in range(MAX_REINTENTOS):
        try:
            pagina.goto(url, timeout=TIMEOUT_NAVEGAR)
            return True
        except Exception as e:
            logger.warning(f"Intento {intento + 1}/{MAX_REINTENTOS} fallido: {e}")
            if intento < MAX_REINTENTOS - 1:
                time.sleep(REINTENTO_ESPERA)
    logger.error(f"Error al navegar a {url} después de {MAX_REINTENTOS} intentos")
    return False


def _esperar_carga(pagina: Page) -> bool:
    """Espera a que la página cargue completamente"""
    try:
        pagina.wait_for_load_state("networkidle", timeout=TIMEOUT_LOAD_STATE)
        return True
    except Exception as e:
        logger.warning(f"Error al esperar carga: {e}")
        return False


def cargar_pagina_principal(pagina: Page) -> bool:
    """Navega a la página principal y espera a que cargue"""
    logger.info("Abriendo la página principal...")

    if not _navegar_con_reintentos(pagina, URL_DESTAQUES):
        return False

    if not _esperar_carga(pagina):
        return False

    try:
        pagina.wait_for_selector(SELECTOR_PUBLICACIONES, timeout=TIMEOUT_LOAD_STATE)
        logger.info("Página principal cargada correctamente.")
        return True
    except Exception as e:
        logger.error(f"No se encontró el selector {SELECTOR_PUBLICACIONES}: {e}")
        return False


def cargar_subpagina(pagina: Page, url: str) -> bool:
    """Navega a una subpágina y espera a que cargue"""
    logger.info(f"Navegando a la subpágina: {url}...")

    if not _navegar_con_reintentos(pagina, url):
        return False

    if not _esperar_carga(pagina):
        return False

    logger.info("Subpágina cargada correctamente.")
    return True


def click_ver_mais(pagina: Page) -> bool:
    """Hace click en el botón 'Ver mais' si existe"""
    try:
        boton = pagina.query_selector("a[href='#ver-mais']")
        if boton:
            logger.info("Botón 'Ver mais' encontrado, haciendo click...")
            boton.click()
            _esperar_carga(pagina)
            return True
    except Exception as e:
        logger.debug(f"Botón 'Ver mais' no encontrado o error: {e}")

    return False