# Funciones para la limpieza y análisis de los datos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def normalizar_columna(df, nombre_columna, reemplazos):
    """
    Estandariza los valores de una columna en un DataFrame y retorna un array con los datos modificados.
    
    Parámetros:
    - df (pd.DataFrame): El DataFrame de pandas.
    - nombre_columna (str): El nombre de la columna a estandarizar.
    - reemplazos (dict): Un diccionario con los reemplazos a aplicar. Las claves son los valores actuales
                         y los valores son los nuevos valores después del reemplazo.
    
    Retorna:
    - np.array: Array con los valores de la columna estandarizados.
    """
    
    print("Antes de la estandarización la columna tiene los siguientes valores únicos:")
    print(df[nombre_columna].unique())

    # Copia de la columna para no modificar el DataFrame original
    columna_modificada = df[nombre_columna].copy()
    
    # Normalizar la columna para uniformidad.
    columna_modificada = columna_modificada.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper()
    
    # Eliminar espacios en blanco al inicio y final del nombre de las categorías
    columna_modificada = columna_modificada.str.strip()
    
    # Reemplazar errores tipográficos y unificar nombres similares.
    columna_modificada = columna_modificada.replace(reemplazos)

    print("-"*80)
    print("Después de la estandarización los valores únicos son:")
    print(columna_modificada.unique())
    
    # Retornar los valores modificados como un array
    return columna_modificada.values

    # Ejemplo de uso
    # Asumiendo que df es tu DataFrame
    # reemplazos = {
    #     'GOBERNACION':'GOBERNACIÓN',
    #     'DPTO': 'GOBERNACIÓN',
    #     'GOBERNACION CALDAS': 'GOBERNACIÓN'
    # }
    # datos_modificados = estandarizar_columna(df, 'PROMOTOR', reemplazos)
    # print(datos_modificados)

#def stats_aggregate(df, by, vars, ):




def tabla_frecuencia(df, column_name, total_name='TOTAL CONTRATOS', percentage_name='PORCENTAJE', ordenar=True):
    """
    Genera una tabla de frecuencia para el DataFrame dado, agrupando por la columna especificada.
    
    Parámetros:
    - df: DataFrame de pandas.
    - column_name: Nombre de la columna por la cual agrupar.
    - total_name: Nombre de la columna para el total de contratos. Default es 'TOTAL CONTRATOS'.
    - percentage_name: Nombre de la columna para el porcentaje. Default es 'PORCENTAJE'.
    - ordenar: Booleano que indica si se deben ordenar los resultados por el total de contratos. Default es True.
    
    Retorna:
    - DataFrame con el total de contratos y el porcentaje para cada categoría del grupo especificado,
      opcionalmente ordenado por el total de contratos.
    """
    # Agrupar por la columna especificada y calcular el total de contratos.
    tabla = df.groupby([column_name]).size().reset_index(name=total_name)
    
    # Opcionalmente, ordenar los resultados por el total de contratos.
    if ordenar:
        tabla = tabla.sort_values(by=total_name, ascending=False)
    
    # Calcular el porcentaje que representa cada tipo de proyecto del total.
    tabla[percentage_name] = np.round((tabla[total_name]/tabla[total_name].sum())*100, 2)
    
    return tabla

    # Ejemplo de uso:
    # Para obtener la tabla ordenada por 'TOTAL CONTRATOS':
    # contratos_tipo_proyecto_ordenado = tabla_frecuencia(df, 'TIPO DE PROYECTO')

    # Para obtener la tabla sin ordenar:
    # contratos_tipo_proyecto_no_ordenado = tabla_frecuencia(df, 'TIPO DE PROYECTO', ordenar=False)

    # print(contratos_tipo_proyecto_ordenado)
    # print(contratos_tipo_proyecto_no_ordenado)


def graficar_barras(df, columna_x, columna_y, titulo='Total de Contratos', 
                    etiqueta_x='x', etiqueta_y='y', figsize=(8,6), horizontal=False):
    """
    Genera un gráfico de barras para visualizar los datos, con opción de orientación horizontal.
    
    Parámetros:
    - df: DataFrame de pandas que contiene los datos a graficar.
    - columna_x: Nombre de la columna que se usará para el eje X.
    - columna_y: Nombre de la columna que se usará para el eje Y.
    - titulo: Título del gráfico.
    - etiqueta_x: Etiqueta para el eje X.
    - etiqueta_y: Etiqueta para el eje Y.
    - figsize: tupla con las dimensiones del gráfico (ancho, largo)
    - horizontal: Booleano que determina la orientación del gráfico (False = vertical, True = horizontal).
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if horizontal:
        barras = ax.barh(df[columna_x], df[columna_y], color='skyblue')
        for barra in barras:
            ancho = barra.get_width()
            ax.annotate('{}'.format(ancho),
                        xy=(ancho, barra.get_y() + barra.get_height() / 2),
                        xytext=(3, 0),  # Desplazamiento horizontal para el texto.
                        textcoords="offset points",
                        ha='left', va='center')
    else:
        barras = ax.bar(df[columna_x], df[columna_y], color='skyblue')
        for barra in barras:
            altura = barra.get_height()
            ax.annotate('{}'.format(altura),
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3),  # Desplazamiento vertical para el texto.
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    # Establecer el título y los nombres de los ejes.
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    
    # Mejorar layout para que todo quepa bien.
    if horizontal:
        plt.yticks(rotation=0, ha='right')  # Rotar etiquetas del eje Y para mejor lectura en gráficos horizontales.
    else:
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas del eje X para mejor lectura en gráficos verticales.
    
    plt.tight_layout()

    # Mostrar el gráfico.
    plt.show()

