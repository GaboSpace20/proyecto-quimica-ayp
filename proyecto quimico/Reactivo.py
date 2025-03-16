class Reactivo:
    def __init__(self, id, nombre, descripcion, costo, categoria, inventario, unidad_medida, caducidad=None, minimo=10, conversiones_posibles=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario = inventario
        self.unidad_medida = unidad_medida
        self.caducidad = caducidad
        self.minimo = minimo
        self.conversiones_posibles = conversiones_posibles or [] # Lista de diccionarios

    def actualizar_inventario(self, cantidad):
        self.inventario = cantidad

    def cambiar_unidad_medida(self, nueva_unidad):
        self.unidad_medida = nueva_unidad

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida}): {self.inventario} disponible"

    def esta_bajo_minimo(self):
        return self.inventario < self.minimo