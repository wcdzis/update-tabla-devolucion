from environment import enviroments
import psycopg2


# puerto de base de datos (0: LOCAL | 1: UAT | 2: PROD)
def ports_database():
    ports = enviroments()

    return {
        "db_host": ports.get("db_host"),
        "db_port": ports.get("db_port"),
        "db_name": ports.get("db_name"),
        "db_user": ports.get("db_user"),
        "db_pss": ports.get("db_pss"),
    }


# Conexion a base de datos
def database_conn():
    config = ports_database().values()
    db_host, db_port, db_name, db_user, db_pss = config

    if None in config:
        raise ValueError("Faltan variables de entorno para la conexión a la BD.")

    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_pss, host=db_host, port=db_port
        )
        print("✅ Conexión exitosa a la base de datos.")
        return conn

    except psycopg2.OperationalError as e:
        print("❌ Error de conexión:", e)
        return None
