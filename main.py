####### MAIN -- Orquestados del scraper #######

from navegador import crear_navegador, cargar_pagina_principal,cerrar_navegador
from extractor import buscar_pdfs_recursivo, obtener_publicaciones, extraer_pdfs
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

        todos_los_resultados = []

        # Por ahora solo mostramos los titulos para verificar 
        # Realizamos un bucle para recorrer las publicaciones y mostrar sus titulos
        for pub in publicaciones[:3]:
            print(f"📌 Título: {pub['titulo']}")

            resultados = buscar_pdfs_recursivo(pagina, pub['url'], pub['titulo'])
            todos_los_resultados.extend(resultados)

        print(f"\n📊 Total PDFs encontrados: {len(todos_los_resultados)}")
        for r in todos_los_resultados:
            print(f"  📄 {r['titulo_pdf'][:50]} → {r['url_pdf'][:50]}")

    # El bloque finally garantiza que el navegador se cerrará correctamente incluso si ocurre un error durante la ejecución del programa
    finally:

        # Creamos un input para que el programa no se cierre automaticamente y podamos ver los resultados por consola
        input("Presiona Enter para cerrar el programa...")

        # Cerramos el navegador y Playwright correctamente
        cerrar_navegador(playwright,navegador)



# Ejecutamos la funcion principal
if __name__ == "__main__":
    main()  


