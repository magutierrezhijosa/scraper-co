############### CONFIGURACION GLOBAL DEL SCRAPER ################

import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URL base de la web que vamos a scrapear
BASE_URL = "https://www.dgeec.medu.pt"

# URL de la pagina principal destaques
URL_DESTAQUES = BASE_URL + "/destaques"

# Nombre del archivo CSV donde guardaremos los resultados
NOMBRE_CSV = "resultados.csv"

# Selector CSS del elemento padre de cada publicacion
SELECTOR_PUBLICACIONES = "span.grelha-item"

# Configuración de navegación
HEADLESS = False
TIMEOUT_NAVEGAR = 30000
TIMEOUT_LOAD_STATE = 30000
MAX_PROFUNDIDAD = 2
MAX_ENLACES_INTERNOS = 5
MAX_PUBLICACIONES = None  # None = todas, número = límite

# Configuración de reintentos
MAX_REINTENTOS = 3
REINTENTO_ESPERA = 2  # segundos entre reintentos

# URLs excluidas y patrones de contenido
PAGINAS_EXCLUIDAS = ["/map", "/destaques", "/contactos", "/sobre"]
PATRONES_CONTENIDO = ["/art/", "/artpub/", "/pagina/"]

