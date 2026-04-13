
###### IMPORTS ######

from playwright.sync_api import sync_playwright


# Creamos una funcion para abrirr la pagina y ver el HTML que nos devuelve
def explorara_pagina():
    # Creamos el contexto donde vamos a abrir el navegador y una vez se ejecute todo el codigo se cerrara automaticamente
    with sync_playwright() as p:

        # Abrimos el navegador Chronium visible (headless=False)
        navegador = p.chromium.launch(headless=False)

        # Creamos una nueva ventana de navegacion
        pagina = navegador.new_page()

        # Le decimos la pagina a la que va a navegar
        print("🌐 Abriendo la página...")
        pagina.goto("https://www.dgeec.medu.pt/destaques")

        # Esperemos a que cargue el contenido principal hasta que la pagina deje de hacer peticiones de red (networkidle)
        pagina.wait_for_load_state("networkidle")
        print("✅ Página cargada!")

        # Guardamos el HTML para inspeccionarlo 
        html = pagina.content()

        # Creamos otro contexto para abrir un archivo y guardar el contenido de la web en este
        with open("pagina.html" , "w" , encoding="utf-8") as file_html:
            
            # Utilizamos la funcion para escribir en nuestro fichero
            file_html.write(html)
        
        print("💾 HTML guardado en pagina.html")

        input("Pulsa ENTER para cerrar el navegdor")

        # Cerramos el navegador
        navegador.close()


# Ejecutamos la funcion 
explorara_pagina()



