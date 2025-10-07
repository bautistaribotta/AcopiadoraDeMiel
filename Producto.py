class Producto:
    def __init__(self, nombre, tipo, cantidad=None, peso=None):
        self.set_nombre = nombre
        self.set_tipo = tipo
        self.set_cantidad = cantidad
        self.set_peso = peso

    # Getter y Setter para nombre
    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        if isinstance(nombre, str) and nombre.strip():
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre del producto debe ser un string no vacío.")

    # Getter y Setter para tipo
    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        if isinstance(tipo, str) and tipo.strip():
            self._tipo = tipo.strip()
        else:
            raise ValueError("El tipo de producto debe ser un string no vacío.")

    # Getter y Setter para cantidad
    def get_cantidad(self):
        return self._cantidad

    def set_cantidad(self, cantidad):
        if cantidad is None:
            self._cantidad = None
        elif isinstance(cantidad, (int, float)):
            self._cantidad = float(cantidad)
        else:
            raise ValueError("La cantidad debe ser un número (float) o estar vacía.")

    # Getter y Setter para peso
    def get_peso(self):
        return self._peso

    def set_peso(self, peso):
        if peso is None:
            self._peso = None
        elif isinstance(peso, (int, float)):
            self._peso = float(peso)
        else:
            raise ValueError("El peso debe ser un número (float) o estar vacío.")

    def __str__(self):
        return (f"Producto: {self.get_nombre()}, Tipo: {self.get_tipo()}, "
                f"Cantidad: {self.get_cantidad()}, Peso: {self.get_peso()}")
