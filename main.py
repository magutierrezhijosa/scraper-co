####### MAIN -- Orquestador del scraper #######

import sys
from navegador import crear_navegador, cargar_pagina_principal, cerrar_navegador
from extractor import obtener_publicaciones
from orquestador import buscar_pdfs_recursivo
from guardador import guardar_csv, cargar_csv_existente
from config import MAX_PUBLICACIONES, logger


def main() -> None:
    """Función principal del programa"""

    playwright, navegador, pagina = crear_navegador()

    try:
        if not cargar_pagina_principal(pagina):
            logger.error("Error al cargar la página principal")
            return

        publicaciones = obtener_publicaciones(pagina)
        logger.info(f"Total publicaciones encontradas: {len(publicaciones)}")

        if MAX_PUBLICACIONES:
            publicaciones = publicaciones[:MAX_PUBLICACIONES]
            logger.info(f"Procesando solo las primeras {MAX_PUBLICACIONES} publicaciones")

        urls_ya_procesadas = cargar_csv_existente()
        urls_ya_guardadas = {r["url_pdf"] for r in urls_ya_procesadas}
        logger.info(f"Ya existen {len(urls_ya_guardadas)} PDFs previamente scrapeados")

        todos_los_resultados = []
        nuevos_resultados = 0

        for i, pub in enumerate(publicaciones, 1):
            logger.info(f"Procesando {i}/{len(publicaciones)}: {pub['titulo'][:50]}")

            resultados = buscar_pdfs_recursivo(pagina, pub["url"], pub["titulo"])

            for r in resultados:
                if r["url_pdf"] not in urls_ya_guardadas:
                    todos_los_resultados.append(r)
                    nuevos_resultados += 1
                    urls_ya_guardadas.add(r["url_pdf"])

        logger.info(f"Total PDFs encontrados: {len(todos_los_resultados)}")
        logger.info(f"PDFs nuevos (no repetidos): {nuevos_resultados}")

        if todos_los_resultados:
            todos_los_resultados.extend(urls_ya_procesadas)
            guardar_csv(todos_los_resultados)
        else:
            logger.info("No se encontraron nuevos PDFs para guardar")

    except KeyboardInterrupt:
        logger.info("Ejecución interrumpida por el usuario")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
    finally:
        if sys.stdin.isatty():
            input("Presiona Enter para cerrar el programa...")
        cerrar_navegador(playwright, navegador)


if __name__ == "__main__":
    main()