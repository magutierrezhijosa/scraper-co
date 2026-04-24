

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


# Funcion que se encarga  de ir a la pagina principal y esperar a que se carguen todo el contenido dinamico de la pagina , hasta poder recoger los selectores 
def cargar_pagina_principal(pagina):

    """Navega a la pagina principal y espera a que cargue"""
    print("🌐 Abriendo la página principal...")

    # Vamos a la pagina que deseamos
    pagina.goto(URL_DESTAQUES)
    # Esperamos a que se cargue el contenido dinamico de la pagina s
    pagina.wait_for_load_state("networkidle")
    # Esperamos a que se carguen los selectores de las publicaciones
    pagina.wait_for_selector(SELECTOR_PUBLICACIONES)
    print("✅ Página principal cargada correctamente.")


# Funcion que se encaga de navegar a una subpagina 
def cargar_subpagina(pagina,url):

    """Navega a una subpagina y espera a que cargue"""
    print(f"🌐 Navegando a la subpágina: {url}...")

    # Vamos a la pagina que deseamos
    pagina.goto(url)
    # Esperamos a que se cargue el contenido dinamico de la subpagina
    pagina.wait_for_load_state("networkidle")
    print("✅ Subpágina cargada correctamente.")


# Funcion encargada de hacer click en "Ver más" para cargar mas publicaciones
def click_ver_mais(pagina):

    # Introducimos el codigo en un try para manejar posibles errores si el boton no se encuentra o no se puede hacer click
    try:

        # Buscamos el boton "Ver más" en la pagina usando el selector CSS
        boton = pagina.query_selector("a[href='#ver-mais']")

        # Si el boton existe, hacemos click en el y esperamos a que se cargue el contenido dinamico de la pagina
        if boton:

            print("  🔽 Botón 'Ver mais' encontrado, haciendo click...")

            # Hacemos click en el boton "Ver más"
            boton.click()

            # Esperamos a que se cargue el contenido dinamico de la pagina
            pagina.wait_for_load_state("networkidle")

            return True

    except:
        pass

    return False