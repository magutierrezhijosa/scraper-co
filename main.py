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

        # Mostramos por consola el numero de publicaciones obtenidas
        print(f"📊 Total publicaciones: {len(publicaciones)}")

        # Por ahora solo mostramos los titulos para verificar 
        # Realizamos un bucle para recorrer las publicaciones y mostrar sus titulos
        for pub in publicaciones:
            print(f"📌 Título: {pub['titulo']}")

    # El bloque finally garantiza que el navegador se cerrará correctamente incluso si ocurre un error durante la ejecución del programa
    finally:

        # Creamos un input para que el programa no se cierre automaticamente y podamos ver los resultados por consola
        input("Presiona Enter para cerrar el programa...")

        # Cerramos el navegador y Playwright correctamente
        cerrar_navegador(playwright,navegador)



# Ejecutamos la funcion principal
if __name__ == "__main__":
    main()  


