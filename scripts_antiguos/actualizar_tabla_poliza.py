import psycopg2
import json

# Configuración de conexión
DB_HOST = "34.48.198.50"
DB_PORT = "30032"
DB_NAME = "vidacash-db-test"
DB_USER = "postgres"
DB_PASSWORD = "Vida2019$."

# ID del registro a modificar
ID_POLIZA = 13847

def actualizar_tabla_devolucion_poliza():
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

        # Obtener el valor actual de tabla_devolucion y periodo_pago
        query_select = """
        SELECT p.id_poliza, p.tabla_devolucion, pd.periodo_pago 
        FROM poliza p
        JOIN poliza_detalle pd ON pd.id_poliza = p.id_poliza AND pd.id_cobertura = 1
        WHERE channel = 'VIDA_CASH_PLUS' AND estado = 3 AND p.id_poliza = %s 
        ORDER BY 1 DESC
        """
        cur.execute(query_select, (ID_POLIZA,))
        result = cur.fetchone()

        if result is None:
            print("❌ No se encontró el registro.")
            return
        
        id_poliza, tabla_devolucion, periodo_pago = result

        # Depuración: Mostrar los valores originales
        print(f"🔹 ID Póliza: {id_poliza}")
        print(f"🔹 Valor original de tabla_devolucion: {tabla_devolucion}")
        print(f"🔹 Valor original de periodo_pago: {periodo_pago}")

        # Convertir tabla_devolucion de JSON string a diccionario Python
        valores = json.loads(tabla_devolucion)

        # Convertir claves a enteros para ordenarlas correctamente
        valores = {int(k): v for k, v in valores.items()}

        # Guardar el valor original de periodo_pago - 1 antes de modificar
        valor_a_duplicar = valores.get(periodo_pago - 1, "0.0000")

        # 1️⃣ Asegurar que el año 2 no tenga 0.0000
        if valores.get(2) == "0.0000" and valores.get(3) != "0.0000":
            valores[2] = valores[3]

        # 2️⃣ Mover todos los valores anteriores al periodo de vigencia un año atrás
        for i in range(2, periodo_pago):
            valores[i] = valores[i + 1]

        # 3️⃣ Duplicar el valor de periodo_pago - 1 en periodo_pago
        valores[periodo_pago-1] = valor_a_duplicar

        # Reconstruir la tabla_devolucion como JSON string
        json_generado = json.dumps(
            {str(k): v for k, v in sorted(valores.items())}, 
            separators=(',', ':')  # 🔹 Elimina espacios innecesarios
        )

        # 4️⃣ Aplicar el formato correcto: Agregar un espacio después de cada coma
        nueva_tabla_devolucion = json_generado.replace(',', ', ')

        # Depuración: Mostrar el nuevo valor antes de actualizar
        print(f"🔹 Nuevo valor de tabla_devolucion: {nueva_tabla_devolucion}")

        # Actualizar la base de datos solo si hubo cambios
        if nueva_tabla_devolucion != tabla_devolucion:
            cur.execute(
                "UPDATE poliza SET tabla_devolucion = %s WHERE id_poliza = %s",
                (nueva_tabla_devolucion, id_poliza)
            )
            conn.commit()
            print("✅ Registro actualizado correctamente.")
        else:
            print("⚠️ No se realizaron cambios.")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        cur.close()
        conn.close()

# Ejecutar la función
actualizar_tabla_devolucion_poliza()
