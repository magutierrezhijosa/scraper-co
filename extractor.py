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

    