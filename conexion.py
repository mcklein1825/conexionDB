import psycopg2
from urllib.parse import urlparse
import os

# ---------------------------------------------------------
# CONFIGURACIÓN
# Reemplaza 'AQUI_TU_CONTRASEÑA' con la contraseña que 
# acabas de copiar del botón "Show password" en Neon.
# ---------------------------------------------------------
DB_PASSWORD = "npg_ZS2iLNo6Uftk" 

# Construcción de la URL de conexión basada en tus datos de pantalla
# Host: ep-twilight-poetry-aea6tyq3.us-east-2.aws.neon.tech (inferido de tu ID de branch)
# DB: neondb
# User: neondb_owner
DATABASE_URL = f"postgresql://neondb_owner:{DB_PASSWORD}@ep-twilight-poetry-aea6tyq3.us-east-2.aws.neon.tech/neondb?sslmode=require"

def conectar_neon():
    try:
        print("🔄 Intentando conectar a Neon...")
        
        # Parsear la URL para extraer los componentes
        url = urlparse(DATABASE_URL)
        
        # Establecer la conexión
        conn = psycopg2.connect(
            host=url.hostname,
            database=url.path[1:],  # Elimina la '/' inicial de '/neondb'
            user=url.username,
            password=url.password,
            port=url.port or 5432,
            sslmode='require'       # Neon exige SSL
        )
        
        print("✅ ¡Conexión exitosa!")
        
        # Crear un cursor para ejecutar consultas
        cur = conn.cursor()
        
        # Consulta de prueba: Obtener versión y usuario actual
        cur.execute("SELECT version(), current_user, current_database();")
        data = cur.fetchone()
        
        print("\n--- Detalles de la Conexión ---")
        print(f"Versión PostgreSQL: {data[0].split(',')[0]}") # Muestra solo la versión
        print(f"Usuario Conectado:  {data[1]}")
        print(f"Base de Datos:      {data[2]}")
        print("-----------------------------\n")
        
        # Cerrar recursos
        cur.close()
        conn.close()
        print("🔒 Conexión cerrada correctamente.")
        
        return True

    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión (Operacional): {e}")
        print("💡 Verifica:")
        print("   1. Que la contraseña sea la correcta (sin espacios extra).")
        print("   2. Que tu IP no esté bloqueada (aunque Neon suele estar abierto por defecto).")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Asegúrate de tener instalado: pip install psycopg2-binary
    conectar_neon()
