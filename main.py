####### MAIN -- Orquestados del scraper #######

from navegador import crear_navegador, cargar_pagina_principal,cerrar_navegador
from extractor import obtener_publicaciones, extraer_pdfs
from guardador import guardar_csv

# Declaramos la funcion principal del programa
def main():

    # Iniciamos el navegador y recogemos las variables empaquetadas que nos devuelve la funcion crear_navegador()
    playwright, navegador , pagina = crear_navegador()

    try:
        # Cargamos la pagina principal
        cargar_pagina_principal(pagina)

        # Obtenemos las publicaciones de la pagina principal
        publicaciones = obtener_publicaciones(pagina)