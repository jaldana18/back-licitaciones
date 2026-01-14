"""
Helper para gestionar conexiones y operaciones con MongoDB Atlas.
Se puede integrar en scraper.py cuando sea necesario guardar datos.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import config
from datetime import datetime


class GestorMongoDB:
    """Clase para gestionar operaciones con MongoDB"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.conectado = False
    
    def conectar(self):
        """Conecta a MongoDB Atlas"""
        try:
            print("🔌 Conectando a MongoDB Atlas...")
            self.client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client[config.DB_NAME]
            self.collection = self.db[config.COLLECTION_NAME]
            self.conectado = True
            print("✓ Conexión a MongoDB exitosa")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ Error al conectar a MongoDB: {e}")
            print("  Verifica tu MONGO_URI en config.py")
            self.conectado = False
            return False
    
    def desconectar(self):
        """Desconecta de MongoDB"""
        if self.client:
            self.client.close()
            self.conectado = False
            print("✓ Conexión a MongoDB cerrada")
    
    def insertar_proceso(self, proceso):
        """Inserta un registro de proceso de licitación"""
        if not self.conectado:
            print("✗ No hay conexión a MongoDB")
            return None
        
        try:
            # Agregar timestamp
            proceso['fecha_guardado'] = datetime.now()
            resultado = self.collection.insert_one(proceso)
            return resultado.inserted_id
        except Exception as e:
            print(f"✗ Error al insertar en MongoDB: {e}")
            return None
    
    def insertar_muchos(self, procesos):
        """Inserta varios registros de procesos"""
        if not self.conectado:
            print("✗ No hay conexión a MongoDB")
            return []
        
        try:
            # Agregar timestamp a cada uno
            for p in procesos:
                p['fecha_guardado'] = datetime.now()
            resultado = self.collection.insert_many(procesos)
            return resultado.inserted_ids
        except Exception as e:
            print(f"✗ Error al insertar en MongoDB: {e}")
            return []
    
    def buscar(self, criterio=None):
        """Busca registros en MongoDB"""
        if not self.conectado:
            print("✗ No hay conexión a MongoDB")
            return []
        
        if criterio is None:
            criterio = {}
        
        try:
            return list(self.collection.find(criterio))
        except Exception as e:
            print(f"✗ Error al buscar en MongoDB: {e}")
            return []
    
    def contar_registros(self):
        """Cuenta el total de registros en la colección"""
        if not self.conectado:
            return 0
        
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"✗ Error al contar registros: {e}")
            return 0
    
    def limpiar_coleccion(self):
        """Elimina todos los registros de la colección (CUIDADO)"""
        if not self.conectado:
            print("✗ No hay conexión a MongoDB")
            return False
        
        try:
            resultado = self.collection.delete_many({})
            print(f"⚠️ Se eliminaron {resultado.deleted_count} registros")
            return True
        except Exception as e:
            print(f"✗ Error al limpiar la colección: {e}")
            return False


def ejemplo_uso():
    """Ejemplo de cómo usar la clase GestorMongoDB"""
    
    # Crear instancia
    mongo = GestorMongoDB()
    
    # Conectar
    if mongo.conectar():
        # Insertar un registro
        proceso = {
            'codigo': 'CP-2024-001',
            'entidad': 'Municipalidad de Quito',
            'objeto': 'Construcción de camino rural',
            'estado': 'ACTIVO',
            'provincia': 'Pichincha',
            'presupuesto': '$100,000.00',
            'fecha': '2024-01-14'
        }
        
        id_insertado = mongo.insertar_proceso(proceso)
        if id_insertado:
            print(f"✓ Registro insertado con ID: {id_insertado}")
        
        # Buscar registros
        registros = mongo.buscar({'estado': 'ACTIVO'})
        print(f"✓ Se encontraron {len(registros)} registros activos")
        
        # Contar total
        total = mongo.contar_registros()
        print(f"✓ Total de registros: {total}")
        
        # Desconectar
        mongo.desconectar()


if __name__ == "__main__":
    ejemplo_uso()
