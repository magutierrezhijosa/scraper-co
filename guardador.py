
############# GUARDADOR - Guardar resultados en CSV ###############

import pandas as pd
from config import NOMBRE_CSV


# Declaramos la funcion que se encarga de guardar los resultados en un archivo CSV
def guardar_csv(resultados):
    """ Recibe una lista de diccionarios y la guarda en un CSV """


    if not resultados:

        print("No hay resultados para guardar.")

        return 

    # Convertimos la lista de diccionarios a un DataFrame de pandas(como una hoja de excel)
    df = pd.DataFrame(resultados, columns=["titulo_publicacion","url_pdf"])

    # Guardamos el DataFrame en un archivo CSV
    df.to_csv(NOMBRE_CSV, index=False, encoding='utf-8-sig')

    print(f"💾 CSV guardado con {len(resultados)} resultados en '{NOMBRE_CSV}'")    