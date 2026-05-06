############# GUARDADOR - Guardar resultados en CSV ###############

from typing import List, Dict, Optional
import pandas as pd
from config import NOMBRE_CSV, logger


def guardar_csv(resultados: List[Dict[str, str]], nombre_csv: Optional[str] = None) -> bool:
    """Recibe una lista de diccionarios y la guarda en un CSV"""

    if not resultados:
        logger.warning("No hay resultados para guardar.")
        return False

    csv_path = nombre_csv or NOMBRE_CSV

    try:
        df = pd.DataFrame(resultados)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info(f"CSV guardado con {len(resultados)} resultados en '{csv_path}'")
        return True
    except Exception as e:
        logger.error(f"Error al guardar CSV: {e}")
        return False


def cargar_csv_existente(nombre_csv: Optional[str] = None) -> List[Dict[str, str]]:
    """Carga un CSV existente y devuelve los PDFs ya scrapeados"""
    csv_path = nombre_csv or NOMBRE_CSV

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        return df.to_dict("records")
    except FileNotFoundError:
        logger.info(f"No existe archivo CSV previo en '{csv_path}'")
        return []
    except Exception as e:
        logger.error(f"Error al cargar CSV existente: {e}")
        return []