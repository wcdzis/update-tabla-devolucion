from environment import enviroments
from db_connection import database_conn
from openpyxl.utils import get_column_letter
import win32com.client
import os

tipo_cambio = enviroments().get("tipo_cambio")

# Conexion global
conn = database_conn()
cursor = conn.cursor()


def get_periodos_cobertura():
    """Obtiene los periodos de cobertura distintos de la BD"""
    query = f"""
    SELECT DISTINCT periodo_cobertura
    FROM precalculo
    WHERE channel = 'VIDA_CASH_PLUS'
        AND tipo_cambio = {tipo_cambio}
        AND id_cobertura = 1
        AND porcentaje > 0
        AND periodo_cobertura < 22
    ORDER BY periodo_cobertura ASC;
    """
    try:
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error al obtener periodos de cobertura: {e}")
        return []


def get_porcetanje_by_periodo(periodo):
    """Obtiene los porcentajes únicos para un periodo dado"""
    query = f"""
    SELECT * 
    FROM get_porcentaje_devolucion(%s, {tipo_cambio});
    """

    try:
        cursor.execute(query, (periodo,))
        return [int(row[0]) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error al obtener porcentajes del periodo {periodo}: {e}")
        return []


def get_porcetanjes_by_periodos():
    """Retorna un diccionario con periodos como claves y sus porcentajes como valores"""
    periodos = get_periodos_cobertura()
    return {periodo: get_porcetanje_by_periodo(periodo) for periodo in periodos}


def obtener_columna_excel(indice):
    return get_column_letter(26 + indice)  # 'Z' es la columna 26

def get_tabla_devolucion_by_periodo_and_porcentaje():
    """
    Lee el archivo Excel TDVCP.xlsx y retorna un diccionario con la tabla de devolución
    organizada por periodo y porcentaje.
    """
    periodo_valores = get_porcetanjes_by_periodos()
    excel_path = os.path.abspath("./assets/TDVCP.xlsx")

    # Conectar a Excel
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    workbook = excel.Workbooks.Open(excel_path)
    sheet = workbook.Sheets("VCP")

    resultados = {}

    for i, (periodo, valores) in enumerate(periodo_valores.items()):
        columna = obtener_columna_excel(i)
        resultados[periodo] = {}

        for valor in valores:
            # print(f"Periodo: {periodo}, Valor: {valor}")

            # Establecer el valor en Z5
            sheet.Range(f"{columna}5").Value = valor

            # Forzar cálculo de la hoja
            sheet.Calculate()

            # Obtener valores recalculados
            inicio_fila = 11
            fin_fila = 11 + (periodo - 1)
            valores_salida = []

            for fila in range(inicio_fila, fin_fila + 1):
                celda_salida = f"{columna}{fila}"
                valor_celda = round(float(sheet.Range(celda_salida).Value) / 100, 4)
                # print(f"{celda_salida}: {valor_celda}")
                valores_salida.append(valor_celda)

            resultados[periodo][valor] = valores_salida

    workbook.Close(SaveChanges=False)
    excel.Quit()
    
    cursor.close()
    conn.close()
    return resultados


periodo = 8
# print(get_periodos_cobertura())
# print(f"Porcentajes devolución ({periodo}): {get_porcetanje_by_periodo(periodo)}")
# print(get_porcetanjes_by_periodos())
# valores_tabla_devolucion = get_tabla_devolucion_by_periodo_and_porcentaje()
# # print(valores_tabla_devolucion[periodo][100])
# # print(valores_tabla_devolucion[16])
# print(valores_tabla_devolucion)

# psql.close()
