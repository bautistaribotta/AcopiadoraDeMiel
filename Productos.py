class Productos:
    def __init__(self, tipo, cantidad_peso):
        self._tipo = tipo
        self._cantidad_peso = cantidad_peso

    # Getter y Setter para tipo
    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        self._tipo = tipo