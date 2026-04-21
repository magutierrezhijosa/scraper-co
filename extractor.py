###### EXTRACTOR -- Analizar HTML y extraer los  datos #######

from bs4 import BeautifulSoup
from config import BASE_URL, SELECTOR_PUBLICACIONES

def obtener_publicaciones(pagina):

    """Exttrae titulo y enlace de cada publicacion de la pagina principal"""

    # Obtenemos el contenido HTML de la pagina
    html = pagina.content()

    # Analizamos el HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Buscamos los elementos que contienen las publicaciones usando el selector CSS
    items = soup.find_all("span", class_="grelha-item")

    # Mostramos en pantala los resultados encontrados 
    print(f"🔍 Encontrados {len(items)} publicaciones")

    # Creamos una lista para almacenar los resultados
    publicaciones = []

    # Recorremos cada elemento encontrado y extraemos el titulo y el enlace
    for item in items:

        # Buscamos el enlace dentro del elemento usando el selector CSS
        enlace = item.find("a", class_="grelha-item-titulo")

        if enlace:

            # Obtenemos el titulo del enlace y lo limpiamos de espacios en blanco
            titulo = enlace.get_text(strip=True)

            # Obtenemos el enlace del elemento
            href = enlace.get("href")

            # Construimos la URL completa de la publicación
            url_completa = BASE_URL + href
            
            # Agregamos el titulo y el enlace a la lista de publicaciones
            publicaciones.append({
                "titulo": titulo, 
                "enlace": url_completa
            })

    return publicaciones


def extraer_pdfs(pagina):
    """Busca todos los enlaces a PDFs en la pagina actual """

    # Obtenemos el contenido HTML de la pagina 
    html = pagina.content()

    # Analizamos el HTML con BeautifulSoup y lo parseamos con html.parser para poder buscar los enlaces a PDFs
    soup = BeautifulSoup(html, "html.parser")

    # Creamos una lista para almacenar los enlaces a PDFs encontrados
    pdfs = []

    # Buscamos todos los enlaces en la pagina 
    for enlace in soup.find_all("a", href=True):

        # Recogemos el enlace 
        href = enlace.get("href")

        # Verificamos si el enlace termina con .pdf (indicando que es un PDF)
        if href.lower().endswith(".pdf"):

            # Construimos la URL completa si es  relativa 
            url_pdf = href if href.startswith("http") else BASE_URL + href

            # Guardamos el titulo del PDF (el texto del enlace)
            titulo_pdf = enlace.get_text(strip=True) or "PDF sin título"

            # Agregamos el PDF a la lista
            pdfs.append({
                "titulo_publicacion": titulo_pdf,
                "url_pdf": url_pdf
            })

    return pdfs

