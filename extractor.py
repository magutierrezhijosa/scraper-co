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


# Declaramos la funcion para extraer los enlaces internos 
def extraer_enlaces_internos(pagina):

    """Busca los enlaces internos que puedan llevar a subpaginas con PDFs"""

    # Obtenemos el contenido de la pagina 
    html = pagina.content()

    # Analizamos el HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # creamos una lista para almacenar los enlaces internos encontrados 
    enlaces = []

    # Buscamos todos los enlaces en la pagina parseada y verificamos si son enlaces internos (que no comienzan con http o https)
    for enlace in soup.find_all("a", href=True):

        # Recogemos el href de cada enlace que recorremos en el bucle
        href = enlace.get("href")

        # Solo nos interesan los enlaces internos qque no sean enlaces PDF (que terminan con .pdf) y que no comienzan con http o https
        if href.startwith("/") and not href.lower().endswwith(".pdf"):

           # Guardamos el enlace completo construyendo la URL completa si es relativa
           url_completa = BASE_URL + href

           # Comprobamos que el enlace no esté ya en la lista de enlaces para evitar duplicados
           if url_completa not in enlaces:

               # Agregamos el enlace a la lista de enlaces internos
                enlaces.append(url_completa) 


    return enlaces

