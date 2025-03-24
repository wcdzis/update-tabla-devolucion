from db_connection import database_conn
from extract_data import get_tabla_devolucion_by_periodo_and_porcentaje, tipo_cambio

conn = database_conn()
cursor = conn.cursor()
data = get_tabla_devolucion_by_periodo_and_porcentaje().items()

# Tabla pivote
def insert_valores_calculo_tabla_devolucion_temp():
    try:
        cursor.execute("TRUNCATE TABLE valores_calculo_tabla_devolucion;")

        # Preparar los datos para la inserción masiva
        insert_data = [
            (periodo, porcentaje, año, valor)
            for periodo, porcentajes in data
            for porcentaje, valores in porcentajes.items()
            for año, valor in enumerate(valores, start=1)
        ]

        # Ejecutar inserción masiva
        cursor.executemany(
            "INSERT INTO valores_calculo_tabla_devolucion (periodo, porcentaje, año, valor) VALUES (%s, %s, %s, %s);",
            insert_data,
        )

        conn.commit()
        # print(
        #     f"{len(insert_data)} registros insertados en valores_calculo_tabla_devolucion"
        # )
        print("Datos insertados en valores_calculo_tabla_devolucion")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# def update_tabla_devolucion_precalculo():
#     try:
#         # insert_valores_calculo_tabla_devolucion_temp()
#         update_data = [
#             (valor, año, periodo, porcentaje)
#             for periodo, porcentajes in data
#             for porcentaje, valores in porcentajes.items()
#             for año, valor in enumerate(valores, start=1)
#         ]

#         query = f"""
#         UPDATE tabla_devolucion_precalculo tdp
#         SET valor = %s
#         FROM precalculo p
#         WHERE tdp.id_precalculo = p.id_precalculo
#           AND p.channel = 'VIDA_CASH_PLUS'
#           AND p.tipo_cambio = {tipo_cambio}
#           AND p.id_cobertura = 1
#           AND tdp.periodo = %s
#           AND p.periodo_cobertura = %s
#           AND p.porcentaje = %s
#         """
#         # print(query)
#         cursor.executemany(query, update_data)
#         conn.commit()
#         print("Datos actualizados en tabla_devolucion_precalculo")
#     except Exception as e:
#         print(f"Error: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()

def update_tabla_devolucion_precalculo():
    try:
        # Cargar los datos en una tabla temporal
        cursor.execute("""
        CREATE TEMP TABLE IF NOT EXISTS tabla_devolucion_temp (
            valor DECIMAL(18,2),
            año INT,
            periodo INT,
            porcentaje INT
        )
        """)
        print("✅ Tabla temporal creada o verificada.")

        # Preparar los datos
        update_data = [
            (valor, año, periodo, porcentaje)
            for periodo, porcentajes in data
            for porcentaje, valores in porcentajes.items()
            for año, valor in enumerate(valores, start=1)
        ]
        
        # Insertar los datos en la tabla temporal
        cursor.executemany("INSERT INTO tabla_devolucion_temp (valor, año, periodo, porcentaje) VALUES (%s, %s, %s, %s)", update_data)
        print("✅ Datos cargados en tabla temporal.")

        # Realizar el update masivo
        query = f"""
        UPDATE tabla_devolucion_precalculo tdp
        SET valor = temp.valor
        FROM tabla_devolucion_temp temp
        INNER JOIN precalculo p ON tdp.id_precalculo = p.id_precalculo
        WHERE p.channel = 'VIDA_CASH_PLUS'
          AND p.tipo_cambio = {tipo_cambio}
          AND p.id_cobertura = 1
          AND tdp.periodo = temp.año
          AND p.periodo_cobertura = temp.periodo
          AND p.porcentaje = temp.porcentaje;
        """
        cursor.execute(query)
        print("✅ Datos actualizados en tabla_devolucion_precalculo.")

        conn.commit()
    except Exception as e:
        print(f"❗ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Ejecutar la función
update_tabla_devolucion_precalculo()



upd = update_tabla_devolucion_precalculo()
print(upd)
# print(len(upd))