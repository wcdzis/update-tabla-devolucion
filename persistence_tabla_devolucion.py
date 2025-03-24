from db_connection import database_conn
from extract_data import get_tabla_devolucion_by_periodo_and_porcentaje, tipo_cambio

conn = database_conn()
cursor = conn.cursor()
data = get_tabla_devolucion_by_periodo_and_porcentaje().items()


# Tabla pivote
def insert_valores_calculo_tabla_devolucion():
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
        # Realizar el update masivo
        # insert_valores_calculo_tabla_devolucion()
        query = f"""
        UPDATE tabla_devolucion_precalculo tdp
        SET valor = vctd.valor
        FROM valores_calculo_tabla_devolucion vctd
        INNER JOIN precalculo p ON tdp.id_precalculo = p.id_precalculo
        WHERE p.channel = 'VIDA_CASH_PLUS'
          AND p.tipo_cambio = {tipo_cambio}
          AND p.id_cobertura = 1
          AND tdp.periodo = vctd.año
          AND p.periodo_cobertura = vctd.periodo
          AND p.porcentaje = vctd.porcentaje;
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


def update_tabla_devolucion_poliza():
    try:
        query = f"""
        UPDATE tabla_devolucion_poliza tdp
        SET valor = vctd.valor
        FROM valores_calculo_tabla_devolucion vctd,
        poliza p,
        poliza_detalle pd
        WHERE tdp.id_poliza = p.id_poliza
        AND tdp.id_poliza = pd.id_poliza
        AND p.channel = 'VIDA_CASH_PLUS'
        AND p.estado = 3
        AND tdp.periodo::TEXT = vctd.año::TEXT
        AND pd.periodo_pago::TEXT = vctd.periodo::TEXT
        AND pd.porcentaje_devolucion = vctd.porcentaje;
        """
        cursor.execute(query)
        print("✅ Datos actualizados en tabla_devolucion_poliza.")
    except Exception as e:
        print(f"❗ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def update_masivo_tablas_devolucion_precalculo_poliza():
    try:
        cursor.execute("CALL actualizar_tablas_devolucion();")
        conn.commit()
        print("✅ Procedimiento actualizar_tablas_devolucion ejecutado correctamente.")
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
