import matplotlib.pyplot as plt
from collections import Counter
import json
import base64
import requests
from GestiondeReactivos import GestorReactivos
from GestiondeExperimentos import GestorExperimentos

class IndicadoresGestion:
     def __init__(self, gestor_experimentos, gestor_reactivos):
        self.gestor_experimentos = gestor_experimentos
        self.gestor_reactivos = gestor_reactivos

     def investigadores_mas_activos(self):
        responsables = [responsable for experimento in self.gestor_experimentos.experimentos for responsable in experimento.responsables]
        contador = Counter(responsables)
        return contador.most_common()

     def experimentos_mas_y_menos_hechos(self):
        nombres_experimentos = [experimento.receta.nombre for experimento in self.gestor_experimentos.experimentos]
        contador = Counter(nombres_experimentos)
        mas_hecho = contador.most_common(1)
        menos_hecho = contador.most_common()[:-2:-1] # Obtener el menos común
        return mas_hecho, menos_hecho

     def reactivos_alta_rotacion(self, top_n=5):
        reactivos_usados = []
        for experimento in self.gestor_experimentos.experimentos:
            for nombre_reactivo in experimento.receta.reactivos_necesarios:
                reactivos_usados.append(nombre_reactivo)
        contador = Counter(reactivos_usados)
        return contador.most_common(top_n)

     def reactivos_mas_desperdicio(self, top_n=3):
        desperdicios = {}
        for experimento in self.gestor_experimentos.experimentos:
            for nombre_reactivo, cantidad_necesaria in experimento.receta.reactivos_necesarios.items():
                reactivo = self.gestor_reactivos.buscar_reactivo(nombre_reactivo)
                if reactivo:
                    desperdicio = cantidad_necesaria * (1 - (reactivo.inventario / (reactivo.inventario + cantidad_necesaria)))
                    if nombre_reactivo in desperdicios:
                        desperdicios[nombre_reactivo] += desperdicio
                    else:
                        desperdicios[nombre_reactivo] = desperdicio
        return sorted(desperdicios.items(), key=lambda item: item[1], reverse=True)[:top_n]

     def experimentos_fallidos(self):
        fallidos = [experimento for experimento in self.gestor_experimentos.experimentos if experimento.resultado and not experimento.resultado.dentro_parametros]
        return len(fallidos)

     def graficar_estadisticas(self):
        # Investigadores más activos
        investigadores, conteos = zip(*self.investigadores_mas_activos())
        plt.figure()
        plt.bar(investigadores, conteos)
        plt.title("Investigadores más activos")
        plt.xlabel("Investigadores")
        plt.ylabel("Número de experimentos")
        plt.xticks(rotation=45)
        plt.show()

        # Experimentos más y menos hechos
        mas_hecho, menos_hecho = self.experimentos_mas_y_menos_hechos()
        plt.figure()
        plt.bar(["Más hecho", "Menos hecho"], [mas_hecho[0][1], menos_hecho[0][1]])
        plt.title("Experimentos más y menos hechos")
        plt.ylabel("Número de veces")
        plt.show()

        # Reactivos de alta rotación
        reactivos, conteos = zip(*self.reactivos_alta_rotacion())
        plt.figure()
        plt.bar(reactivos, conteos)
        plt.title("Reactivos de alta rotación")
        plt.xlabel("Reactivos")
        plt.ylabel("Número de veces usados")
        plt.xticks(rotation=45)
        plt.show()

        # Reactivos con más desperdicio
        reactivos, desperdicios = zip(*self.reactivos_mas_desperdicio())
        plt.figure()
        plt.bar(reactivos, desperdicios)
        plt.title("Reactivos con más desperdicio")
        plt.xlabel("Reactivos")
        plt.ylabel("Desperdicio total")
        plt.xticks(rotation=45)
        plt.show()

        # Experimentos fallidos
        fallidos = self.experimentos_fallidos()
        plt.figure()
        plt.bar(["Fallidos", "Exitosos"], [fallidos, len(self.gestor_experimentos.experimentos) - fallidos])
        plt.title("Experimentos fallidos vs. exitosos")
        plt.ylabel("Número de experimentos")
        plt.show()

# ... (tus clases Reactivo, GestorReactivos, Receta, Experimento, GestorExperimentos, ResultadoExperimento, IndicadoresGestion)

# Crear instancias de GestorReactivos y GestorExperimentos
url_reactivos = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/reactivos.json" 
token = "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" 
gestor_reactivos = GestorReactivos()
gestor_reactivos.cargar_desde_api(url_reactivos, token)

url_recetas = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/recetas.json"
url_experimentos = "https://raw.githubusercontent.com/GaboSpace20/api-proyecto/refs/heads/main/experimentos.json" 
gestor_experimentos = GestorExperimentos(gestor_reactivos, url_recetas, url_experimentos)

# Crear instancia de IndicadoresGestion
indicadores = IndicadoresGestion(gestor_experimentos, gestor_reactivos)

# Utilizar la instancia de IndicadoresGestion
print("Investigadores más activos:", indicadores.investigadores_mas_activos())
print("Experimentos más y menos hechos:", indicadores.experimentos_mas_y_menos_hechos())
print("Reactivos de alta rotación:", indicadores.reactivos_alta_rotacion())
print("Reactivos con más desperdicio:", indicadores.reactivos_mas_desperdicio())
print("Experimentos fallidos:", indicadores.experimentos_fallidos())

indicadores.graficar_estadisticas()