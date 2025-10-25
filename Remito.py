from datetime import *

class Remito:
    """Modelo de datos para Remito"""
    contador_id = 1

    def __init__(self, cliente, total, estado="Pendiente", numero=None, fecha=None, id_db=None):
        self.id_db = id_db
        self.numero = numero if numero else f"REM-2025-{str(Remito.contador_id).zfill(3)}"
        if not numero:
            Remito.contador_id += 1
        self.fecha = fecha if fecha else datetime.now().strftime("%d/%m/%Y")
        self.cliente = cliente
        self.total = total
        self.estado = estado

    def get_datos_tabla(self):
        """Retorna tupla para mostrar en tabla"""
        return self.numero, self.fecha, self.cliente, f"${self.total:,.2f}", self.estado

    @staticmethod
    def desde_db(tupla_db):
        """Crear objeto Remito desde tupla de base de datos"""
        # tupla_db: (id, numero, fecha, nombre_cliente, total, estado)
        return Remito(
            cliente=tupla_db[3],
            total=tupla_db[4],
            estado=tupla_db[5],
            numero=tupla_db[1],
            fecha=tupla_db[2],
            id_db=tupla_db[0]
        )
