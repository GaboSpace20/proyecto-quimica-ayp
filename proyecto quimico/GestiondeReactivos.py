import json
import requests
import Reactivo


class GestorReactivos:
   
     def __init__(self, ruta_archivo=None, api_url=None):
        self.reactivos = {}
        self.ruta_archivo = ruta_archivo
        self.api_url = api_url
        if ruta_archivo:
            self.cargar_desde_archivo()
        elif api_url:
            self.cargar_desde_api()
     def agregar_reactivo(self, reactivo):
        self.reactivos[reactivo.nombre] = reactivo

     def eliminar_reactivo(self, nombre):
        if nombre in self.reactivos:
            del self.reactivos[nombre]

     def editar_reactivo(self, nombre, **kwargs):
        if nombre in self.reactivos:
            for clave, valor in kwargs.items():
                setattr(self.reactivos[nombre], clave, valor)

     def buscar_reactivo(self, nombre):
        return self.reactivos.get(nombre)

     def listar_reactivos(self):
        return list(self.reactivos.values())

     def verificar_minimos(self):
        reactivos_bajo_minimo = [reactivo for reactivo in self.reactivos.values() if reactivo.esta_bajo_minimo()]
        return reactivos_bajo_minimo

     def cargar_desde_archivo(self):
        try:
            with open(self.ruta_archivo, 'r') as archivo:
                datos = json.load(archivo)
                for nombre, info in datos.items():
                    self.agregar_reactivo(Reactivo(**info))
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.ruta_archivo}")

     def guardar_en_archivo(self):
        datos = {nombre: reactivo.__dict__ for nombre, reactivo in self.reactivos.items()}
        with open(self.ruta_archivo, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
     def cargar_desde_api(self, url_api, token_github=None):
        try:
            headers = {}
            if token_github:
                headers['Authorization'] = f'Bearer {token_github}' #cambio a Bearer, para el token de github_pat

            respuesta = requests.get(url_api, headers=headers)
            respuesta.raise_for_status()
            datos = respuesta.json()

            for info in datos:
                # Asegúrate de que los nombres de los campos coincidan exactamente con los atributos de la clase Reactivo
                self.agregar_reactivo(Reactivo(**info))

        except requests.exceptions.RequestException as e:
            print(f"Error al cargar desde la API: {e}")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

# Ejemplo de uso:
url_api = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/reactivos.json"
token = "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" 
gestor = GestorReactivos()
gestor.cargar_desde_api(url_api, token_github=token)

for reactivo in gestor.listar_reactivos():
    print(reactivo)