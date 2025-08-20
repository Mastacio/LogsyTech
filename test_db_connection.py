#!/usr/bin/env python3
import psycopg2
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'postgreSql',
    'port': 5432,
    'user': 'UserSystem',
    'password': 'Wqh5$Rsu67e.',
    'database': 'LogsyTech'
}

def test_connection():
    try:
        print("Probando conexión a PostgreSQL...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"Puerto: {DB_CONFIG['port']}")
        print(f"Usuario: {DB_CONFIG['user']}")
        print(f"Base de datos: {DB_CONFIG['database']}")
        
        # Intentar conexión
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexión exitosa!")
        
        # Ejecutar una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Versión de PostgreSQL: {version[0]}")
        
        # Verificar si la base de datos LogsyTech existe
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"Base de datos actual: {current_db[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    test_connection()
