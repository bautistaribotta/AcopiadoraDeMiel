class Clientes:
    def __init__(self, nombre_completo, localidad, telefono, cantidad_colmenas, codigo_renapa, factura_produccion):
        self.set_nombre_completo(nombre_completo)
        self.set_localidad(localidad)
        self.set_telefono(telefono)
        self.set_cantidad_colmenas(cantidad_colmenas)
        self.set_codigo_renapa(codigo_renapa)
        self.set_factura_produccion(factura_produccion)


    # Getter y Setter para nombre_completo
    def get_nombre_completo(self):
        return self._nombre_completo

    def set_nombre_completo(self, nombre):
        if isinstance(nombre, str) and len(nombre.strip()) >= 3:
            self._nombre_completo = nombre.strip()
        else:
            raise ValueError("El nombre completo debe ser un string con al menos 3 letras.")


    # Getter y Setter para localidad
    def get_localidad(self):
        return self._localidad

    def set_localidad(self, localidad):
        if isinstance(localidad, str) and localidad.strip():
            self._localidad = localidad.strip()
        else:
            raise ValueError("La localidad no puede estar vacía.")


    # Getter y Setter para teléfono
    def get_telefono(self):
        return self._telefono

    def set_telefono(self, telefono):
        if isinstance(telefono, int):
            self._telefono = telefono
        else:
            raise ValueError("El teléfono debe ser un número entero sin comas ni puntos.")


    # Getter y Setter para cantidad_colmenas
    def get_cantidad_colmenas(self):
        return self._cantidad_colmenas

    def set_cantidad_colmenas(self, cantidad):
        if isinstance(cantidad, int) and cantidad >= 0:
            self._cantidad_colmenas = cantidad
        else:
            raise ValueError("La cantidad de colmenas debe ser un número entero no negativo.")


    # Getter y Setter para código RENAPA
    def get_codigo_renapa(self):
        return self._codigo_renapa

    def set_codigo_renapa(self, codigo):
        self._codigo_renapa = str(codigo).strip()


    # Getter y Setter para factura de producción
    def get_factura_produccion(self):
        return self._factura_produccion

    def set_factura_produccion(self, factura):
        self._factura_produccion = str(factura).strip()

    def __str__(self):
        return (f"Cliente: {self.get_nombre_completo()}, Localidad: {self.get_localidad()}, Teléfono: {self.get_telefono()}, "
                f"Colmenas: {self.get_cantidad_colmenas()}, RENAPA: {self.get_codigo_renapa()}, Factura: {self.get_factura_produccion()}")
