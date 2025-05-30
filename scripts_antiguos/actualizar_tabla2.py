import psycopg2
import re

# Configuración de conexión
DB_HOST = "34.48.198.50"
DB_PORT = "30032"
DB_NAME = "vidacash-db-test"
DB_USER = "postgres"
DB_PASSWORD = "Vida2019$."

# ID del registro a modificar
ID_PRECALCULO = 12619548

def actualizar_tabla_devolucion():
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

        # Obtener el valor actual de tabla_devolucion y periodo_cobertura
        cur.execute("SELECT tabla_devolucion, periodo_cobertura FROM precalculo WHERE id_precalculo = %s", (ID_PRECALCULO,))
        result = cur.fetchone()

        if result is None:
            print("No se encontró el registro.")
            return
        
        tabla_devolucion, periodo_cobertura = result

        # Depuración: Mostrar los valores originales
        print(f"Valor original de tabla_devolucion: {tabla_devolucion}")
        print(f"Valor original de periodo_cobertura: {periodo_cobertura}")

        # Extraer valores con regex
        pattern = r'(\d+)=(\d+\.?\d*%)'  # Extrae correctamente pares clave-valor
        valores = dict(re.findall(pattern, tabla_devolucion))

        # Convertir claves a enteros para ordenarlas correctamente
        valores = {int(k): v for k, v in valores.items()}

        # Copia del valor original de periodo_cobertura - 1 antes de modificar la tabla
        valor_a_duplicar = valores.get(periodo_cobertura - 1, "0%")
        print(f"Valor a duplicar valor_a_duplicar: {valor_a_duplicar}")

        # 1️⃣ Asegurar que el año 2 no tenga 0%
        if valores.get(2) == "0%" and valores.get(3) != "0%":
            valores[2] = valores[3]  # Copiar el valor del año 3 al año 2

        # 2️⃣ Mover todos los valores anteriores al periodo de cobertura un año atrás
        for i in range(2, periodo_cobertura):
            valores[i] = valores[i + 1]

        # 3️⃣ Duplicar el valor de periodo_cobertura - 1 (de la tabla original) en periodo_cobertura
        valores[periodo_cobertura-1] = valor_a_duplicar

        # Reconstruir la cadena modificada
        nueva_tabla_devolucion = "{" + ", ".join(f"{k}={v}" for k, v in sorted(valores.items())) + "}"

        # Depuración: Mostrar el nuevo valor antes de actualizar
        print(f"Nuevo valor de tabla_devolucion: {nueva_tabla_devolucion}")

        # Actualizar la base de datos si hubo cambios
        if nueva_tabla_devolucion != tabla_devolucion:
            cur.execute(
                "UPDATE precalculo SET tabla_devolucion = %s WHERE id_precalculo = %s",
                (nueva_tabla_devolucion, ID_PRECALCULO)
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
actualizar_tabla_devolucion()
