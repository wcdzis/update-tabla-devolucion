import psycopg2
import re
from datetime import datetime

# Configuración de conexión
DB_HOST = "34.48.198.50"
DB_PORT = "30032"
DB_NAME = "vidacash-db-test"
DB_USER = "postgres"
DB_PASSWORD = "Vida2019$."

# Tamaño del batch para evitar consumo excesivo de memoria
BATCH_SIZE = 10  # Procesar 1000 registros por iteración

def actualizar_tabla_devolucion_masivo():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        # Obtener todos los registros que cumplen con la condición en lotes
        query_select = """
        SELECT id_precalculo, tabla_devolucion, periodo_cobertura 
        FROM precalculo 
        WHERE channel='VIDA_CASH_PLUS' AND tipo_cambio='3.718' AND id_cobertura = 1
        """
        print(f"🔄 tiempo antes de ejecucion query => ", datetime.now())
        cur.execute(query_select)
        print(f"🔄 tiempo despues de ejecucion query => ", datetime.now())

        registros_actualizados = 0
        batch = []

        # Procesar cada fila
        for row in cur.fetchall():
            id_precalculo, tabla_devolucion, periodo_cobertura = row

            # Extraer valores con regex
            pattern = r'(\d+)=(\d+\.?\d*%)'  # Extrae correctamente pares clave-valor
            valores = dict(re.findall(pattern, tabla_devolucion))

            # Convertir claves a enteros para ordenarlas correctamente
            valores = {int(k): v for k, v in valores.items()}

            # Guardar el valor original de periodo_cobertura - 1 antes de modificar
            valor_a_duplicar = valores.get(periodo_cobertura - 1, "0%")

            # 1️⃣ Asegurar que el año 2 no tenga 0%
            if valores.get(2) == "0%" and valores.get(3) != "0%":
                valores[2] = valores[3]

            # 2️⃣ Mover todos los valores anteriores al periodo de cobertura un año atrás
            for i in range(2, periodo_cobertura):
                valores[i] = valores[i + 1]

            # 3️⃣ Duplicar el valor de periodo_cobertura - 1 en periodo_cobertura
            valores[periodo_cobertura-1] = valor_a_duplicar

            # Reconstruir la cadena modificada
            nueva_tabla_devolucion = "{" + ", ".join(f"{k}={v}" for k, v in sorted(valores.items())) + "}"

            # Si el valor cambió, agregar al batch para actualización
            if nueva_tabla_devolucion != tabla_devolucion:
                batch.append((nueva_tabla_devolucion, id_precalculo))

            # Ejecutar batch cada BATCH_SIZE registros
            if len(batch) >= BATCH_SIZE:
                cur.executemany("UPDATE precalculo SET tabla_devolucion = %s WHERE id_precalculo = %s", batch)
                print(f"🔄 tiempo antes de => ", datetime.now())
                conn.commit()
                print(f"🔄 tiempo despues de => ", datetime.now())
                registros_actualizados += len(batch)
                print(f"✅ {registros_actualizados} registros actualizados...")
                batch = []

        # Actualizar el último batch si queda algo pendiente
        if batch:
            cur.executemany("UPDATE precalculo SET tabla_devolucion = %s WHERE id_precalculo = %s", batch)
            conn.commit()
            registros_actualizados += len(batch)

        print(f"✅ Proceso finalizado. Total de registros actualizados: {registros_actualizados}")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        cur.close()
        conn.close()

# Ejecutar la función
actualizar_tabla_devolucion_masivo()
