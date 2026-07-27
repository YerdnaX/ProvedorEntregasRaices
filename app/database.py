import os
from contextlib import contextmanager

import pymssql
from dotenv import load_dotenv

load_dotenv()


def crear_configuracion_db() -> dict:
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE", "tiusr15pl_ProvedoresRaicesBosque")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = int(os.getenv("DB_PORT", "1433"))

    return {
        "server": server,
        "user": user,
        "password": password,
        "database": database,
        "port": port,
        "login_timeout": 30,
        "timeout": 30,
        "as_dict": True,
    }


@contextmanager
def obtener_conexion():
    conexion = pymssql.connect(**crear_configuracion_db())
    try:
        yield conexion
    finally:
        conexion.close()
