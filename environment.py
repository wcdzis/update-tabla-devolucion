from dotenv import load_dotenv
import os

load_dotenv()


def enviroments():
    type = os.getenv("TYPE_ENV")
    environment = "LOCAL" if type == "0" else "UAT" if type == "1" else "PROD"

    return {
        "db_host": os.getenv(f"DB_HOST_{environment}"),
        "db_port": os.getenv(f"DB_PORT_{environment}"),
        "db_name": os.getenv(f"DB_NAME_{environment}"),
        "db_user": os.getenv(f"DB_USER_{environment}"),
        "db_pss": os.getenv(f"DB_PASSWORD_{environment}"),
        "tipo_cambio": os.getenv("TIPO_CAMBIO"),
    }
