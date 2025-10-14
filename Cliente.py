class Cliente:
    """Modelo de datos para Cliente"""

    def __init__(self, nombre, localidad, direccion="", colmenas=0, renapa="", factura=False, id_db=None):
        self.id_db = id_db  # ID de la base de datos
        self.nombre = nombre
        self.email = f"{nombre.lower().replace(' ', '.')}@email.com"
        self.localidad = localidad
        self.direccion = direccion
        self.colmenas = colmenas
        self.renapa = renapa
        self.factura = factura
        self.telefono = "+54 351 000-0000"

    def get_datos_tabla(self):
        """Retorna tupla para mostrar en tabla"""
        return self.id_db, self.nombre, self.email, self.telefono, self.localidad

    @staticmethod
    def desde_db(tupla_db):
        """Crear objeto Cliente desde tupla de base de datos"""
        # tupla_db: (id, nombre, email, telefono, localidad, direccion, colmenas, renapa, factura, fecha_registro)
        cliente = Cliente(
            nombre=tupla_db[1],
            localidad=tupla_db[4],
            direccion=tupla_db[5],
            colmenas=tupla_db[6],
            renapa=tupla_db[7],
            factura=bool(tupla_db[8]),
            id_db=tupla_db[0]
        )
        cliente.email = tupla_db[2]
        cliente.telefono = tupla_db[3]
        return cliente