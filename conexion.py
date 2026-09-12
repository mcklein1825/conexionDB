import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Opción 1: Usar variable de entorno (RECOMENDADO - más seguro)
DATABASE_URL = os.getenv("DATABASE_URL")

# Opción 2: Connection string directo (solo para desarrollo)
# Reemplaza con tu connection string real de Neon
# Lo encuentras en: https://console.neon.tech -> tu proyecto -> Connection Details
if not DATABASE_URL:
    DATABASE_URL = "postgresql://usuario:password@ep-old-morning-ae89tbp3.us-east-2.aws.neon.tech/neondb?sslmode=require"
    # ⚠️ IMPORTANTE: 
    # 1. Reemplaza 'usuario' con tu username de Neon
    # 2. Reemplaza 'password' con tu password (NO uses tu email/password de login)
    # 3. El host debe ser como: ep-xxx-xxx.region.aws.neon.tech
    # 4. Asegúrate de incluir ?sslmode=require

def conectar():
    """Establece conexión con Neon DB"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conexión exitosa a Neon DB!")
        
        # Crear cursor para ejecutar consultas
        cur = conn.cursor()
        
        # Verificar conexión obteniendo versión de PostgreSQL
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"📊 Versión de PostgreSQL: {db_version[0][:50]}...")
        
        # Ejemplo: listar tablas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tablas = cur.fetchall()
        print(f"📁 Tablas encontradas: {[t[0] for t in tablas]}")
        
        cur.close()
        return conn
        
    except OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Posibles causas:")
        print("   1. Connection string incorrecto")
        print("   2. Password inválido (usa el de DB, no el de tu cuenta)")
        print("   3. Firewall/IP restringida (revisa settings en Neon console)")
        print("   4. SSL no habilitado (asegúrate de usar ?sslmode=require)")
        return None

if __name__ == "__main__":
    conexion = conectar()
    if conexion:
        print("\n✅ ¡Conexión establecida correctamente!")
        conexion.close()
