class Producto:
    """Modelo de datos para Producto"""
    contador_id = 1

    def __init__(self, nombre, categoria, precio, stock, codigo=None, id_db=None):
        self.id_db = id_db
        self.codigo = codigo if codigo else f"PRD{str(Producto.contador_id).zfill(3)}"
        if not codigo:
            Producto.contador_id += 1
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def get_datos_tabla(self):
        """Retorna tupla para mostrar en tabla"""
        return self.codigo, self.nombre, self.categoria, f"${self.precio:,.2f}", self.stock

    @staticmethod
    def desde_db(tupla_db):
        """Crear objeto Producto desde tupla de base de datos"""
        # tupla_db: (id, codigo, nombre, categoria, precio, stock, fecha_registro)
        return Producto(
            nombre=tupla_db[2],
            categoria=tupla_db[3],
            precio=tupla_db[4],
            stock=tupla_db[5],
            codigo=tupla_db[1],
            id_db=tupla_db[0]
        )

