###### EXTRACTOR -- Analizar HTML y extraer los  datos #######

from bs4 import BeautifulSoup
from config import BASE_URL, SELECTOR_PUBLICACIONES
from navegador import click_ver_mais

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

def buscar_pdfs_recursivo(pagina, url, titulo_publicacion, profundidad=0):

    """
    + Busca PDFs en una página
    + Si no encuentra PDFs busca enlcaes internos y entra en ellos
    + La profundidad evita bucles infinitos
    """

    # Condicion de parada 1 - eevitar profundidad infinita
    if profundidad > 2:

        return []
    
    # Condicion de parada 2 - ignorar publicaciones sin titulo 
    if not titulo_publicacion.strip():

        return []

    # Mostramos por consola el enlace que estamos analizando y la profundidad actual del bucle recursivo para tener una idea de la navegación que está realizando el programa
    print(f"{'  ' * profundidad}🔍 Buscando PDFs en: {url[:60]}")

    # Creamos una lista para almacenar los PDFs encontrados en esta página y sus subpáginas
    resultados = []

    # Navegamos a la URL
    pagina.goto(url)

    # EEsperamos a que se cargue el contenido dinámico de la página
    pagina.wait_for_load_state("networkidle")

    # Hacemos click en "Ver más" para cargar más publicaciones si el botón existe
    click_ver_mais(pagina)

    # Buscamos PDFs en la página actual
    pdfs = extraer_pdfs(pagina)


    if pdfs:

        # Condicion de parada 3 - encontramos PDFs , no seguimos buscando
        print(f"  {'  ' * profundidad}✅ {len(pdfs)} PDF(s) encontrados")

        # Recorremos los PDFs encontrados y agregamos el título de la publicación a cada uno para tener un contexto de donde se encontró el PDF
        for pdf in pdfs:

            resultados.append({
                "titulo_publicacion": titulo_publicacion,
                "titulo_pdf": pdf["titulo_publicacion"],
                "url_pdf": pdf["url_pdf"]
            })      

    else:

        # No hay PDFs -  buscamos enlaces internos y entramos en ellos
        enlaces = extraer_enlaces_internos(pagina)

        print(f"  {'  ' * profundidad}↪ Sin PDFs, explorando {len(enlaces)} enlaces internos...")

        # Limitamos el número de enlaces internos a explorar para evitar demasiada recursión
        for enlace in enlaces[:5]:

            sub_resultados = buscar_pdfs_recursivo(pagina, enlace, titulo_publicacion, profundidad + 1)

            resultados.extend(sub_resultados)

    return resultados


