

############# NAVEGADOR - Funciones relacionadas con Playwright

from playwright.sync_api import sync_playwright
from config import URL_DESTAQUES, SELECTOR_PUBLICACIONES

# Creamos la funcion que crea el navegador 
def crear_navegador():

    """Inicia playright y devuelve el navegador y el contexto"""
    playright = sync_playwright().start()

    # Abrimos un nuevo navegador 
    navegador = playright.chromium.launch(headless=False)

    # Abrimos una nueva pagina 
    pagina = navegador.new_page()

    return playright, navegador, pagina


# Funcion encargada de cerrar el navegador y el contexto
def cerrar_navegador(playright,navegador):
    """Cierra el navegador y Playwright correctamente"""
    navegador.close()
    playright.stop()


