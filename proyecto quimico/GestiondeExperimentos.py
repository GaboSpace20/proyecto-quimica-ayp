import json
import random
import requests
from GestiondeResultados import ResultadoExperimento


class Receta:
     def __init__(self, id_receta, nombre, objetivo, reactivos_necesarios, procedimiento, valores_calculo=None, ecuaciones=None, valores_aceptables=None):
        self.id_receta = id_receta
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos_necesarios = reactivos_necesarios
        self.procedimiento = procedimiento
        self.valores_calculo = valores_calculo or {} # Diccionario {nombre_valor: unidad}
        self.ecuaciones = ecuaciones or {} # Diccionario {nombre_valor: ecuacion (string)}
        self.valores_aceptables = valores_aceptables or {} # Diccionario {nombre_valor: (min, max)}
        
     def __str__(self):
        
        return f"Receta: {self.nombre} (ID: {self.id_receta})"

class Experimento:
      def __init__(self, receta, responsables, fecha, costo_asociado=0, resultado=None):
        self.receta = receta
        self.responsables = responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado
      def __str__(self):
        return f"Experimento: {self.receta.nombre} ({self.fecha})"     

class GestorExperimentos:
     def __init__(self, gestor_reactivos, url_recetas, url_experimentos):
        self.gestor_reactivos = gestor_reactivos
        self.recetas = self.cargar_recetas(url_recetas)
        self.experimentos = self.cargar_experimentos(url_experimentos)
        self.url_recetas = url_recetas
        self.url_experimentos = url_experimentos
        
        url_recetas = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/recetas.json"
        url_experimentos = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/experimentos.json"
        gestor_experimentos = GestorExperimentos(gestor_reactivos, url_recetas, url_experimentos)
    
     def registrar_resultados(self, experimento_id, resultados_obtenidos):
        experimento = self.experimentos[experimento_id]
        resultado = ResultadoExperimento(experimento, resultados_obtenidos)
        experimento.resultado = resultado
        self.guardar_experimentos()
        return resultado
     def cargar_experimentos(self, url_experimentos):
        try:
            respuesta = requests.get(url_experimentos)
            respuesta.raise_for_status()
            datos = respuesta.json()
            return [Experimento(**info) for info in datos]
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar experimentos: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON de experimentos: {e}")
            return []

     def agregar_receta(self, receta):
        self.recetas[receta.id_receta] = receta
        self.guardar_recetas()

     def eliminar_receta(self, id_receta):
        if id_receta in self.recetas:
            del self.recetas[id_receta]
            self.guardar_recetas()

     def editar_receta(self, id_receta, **kwargs):
        if id_receta in self.recetas:
            for clave, valor in kwargs.items():
                setattr(self.recetas[id_receta], clave, valor)
            self.guardar_recetas()

     def buscar_receta(self, id_receta):
        return self.recetas.get(id_receta)

     def listar_recetas(self):
        return list(self.recetas.values())

     def realizar_experimento(self, receta_id, responsables, fecha):
        receta = self.buscar_receta(receta_id)
        if not receta:
            return "Receta no encontrada."

        costo_total = 0
        for nombre_reactivo, cantidad_necesaria in receta.reactivos_necesarios.items():
            reactivo = self.gestor_reactivos.buscar_reactivo(nombre_reactivo)
            if not reactivo or reactivo.inventario < cantidad_necesaria:
                return f"Reactivo {nombre_reactivo} insuficiente o no encontrado."

            costo_total += reactivo.costo * cantidad_necesaria
            reactivo.actualizar_inventario(reactivo.inventario - cantidad_necesaria)

            # Simulación de error (0.1% - 22.5%)
            error = random.uniform(0.001, 0.225)
            costo_total += costo_total * error
            reactivo.actualizar_inventario(reactivo.inventario - (cantidad_necesaria * error))

        experimento = Experimento(receta, responsables, fecha, costo_total)
        self.experimentos.append(experimento)
        self.gestor_reactivos.guardar_en_archivo()
        self.guardar_experimentos()

        return experimento

     def cargar_recetas(self, url_recetas):
        try:
            respuesta = requests.get(url_recetas)
            respuesta.raise_for_status()
            datos = respuesta.json()
            return {int(receta["id_receta"]): Receta(**receta) for receta in datos}
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar recetas: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON de recetas: {e}")
            return {}

     def cargar_experimentos(self, url_experimentos):
        try:
            respuesta = requests.get(url_experimentos)
            respuesta.raise_for_status()
            datos = respuesta.json()
            return [Experimento(**info) for info in datos]
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar experimentos: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON de experimentos: {e}")
            return []
     
     def guardar_recetas(self):
        datos = {receta.id_receta: receta.__dict__ for receta in self.recetas.values()}
        try:
            with open(self.url_recetas, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar recetas: {e}")
     
     def guardar_experimentos(self):
        datos = [experimento.__dict__ for experimento in self.experimentos]
        try:
            with open(self.url_experimentos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar experimentos: {e}")
