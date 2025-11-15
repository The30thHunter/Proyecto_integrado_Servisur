import pandas as pd
from django.apps import apps

def exportar_bd_a_excel(ruta_archivo="servisur_export.xlsx"):
    """
    Exporta la información de la base de datos a un archivo Excel,
    con una hoja por cada modelo.
    """
    # Diccionario de modelos a exportar
    modelos = {
        "Clientes": apps.get_model("Base_Datos", "Cliente"),
        "Marcas": apps.get_model("Base_Datos", "Marca"),
        "Modelos": apps.get_model("Base_Datos", "Modelo"),
        "Dispositivos": apps.get_model("Base_Datos", "Dispositivo"),
        "Tipos_de_Falla": apps.get_model("Base_Datos", "Tipo_Falla"),
        "Pedidos": apps.get_model("Base_Datos", "Pedido"),
    }

    # Crear un escritor de Excel
    with pd.ExcelWriter(ruta_archivo, engine="openpyxl") as writer:
        for nombre_hoja, modelo in modelos.items():
            # Obtener todos los registros del modelo
            registros = modelo.objects.all().values()
            # Convertir a DataFrame
            df = pd.DataFrame(list(registros))
            # Escribir en una hoja del Excel
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)

    return f"Archivo Excel creado en: {ruta_archivo}"