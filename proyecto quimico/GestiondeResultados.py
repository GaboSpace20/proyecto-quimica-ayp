import matplotlib.pyplot as plt

class ResultadoExperimento:
    def __init__(self, experimento, resultados_obtenidos):
        self.experimento = experimento
        self.resultados_obtenidos = resultados_obtenidos # Diccionario {nombre_valor: valor}
        self.resultados_calculados = {}
        self.dentro_parametros = True
        self.analizar_resultados()

    def analizar_resultados(self):
        receta = self.experimento.receta
        for nombre_valor, ecuacion in receta.ecuaciones.items():
            try:
                # Evaluar la ecuación usando los resultados obtenidos
                self.resultados_calculados[nombre_valor] = eval(ecuacion, self.resultados_obtenidos)
                # Validar contra los valores aceptables
                if nombre_valor in receta.valores_aceptables:
                    min_val, max_val = receta.valores_aceptables[nombre_valor]
                    if not (min_val <= self.resultados_calculados[nombre_valor] <= max_val):
                        self.dentro_parametros = False
            except Exception as e:
                print(f"Error al calcular {nombre_valor}: {e}")
                self.dentro_parametros = False

    def graficar_resultados(self):
        receta = self.experimento.receta
        for nombre_valor, valor_calculado in self.resultados_calculados.items():
            if nombre_valor in receta.valores_aceptables:
                min_val, max_val = receta.valores_aceptables[nombre_valor]
                plt.figure()
                plt.bar(["Calculado", "Mínimo", "Máximo"], [valor_calculado, min_val, max_val])
                plt.title(f"Resultados de {nombre_valor} para {receta.nombre}")
                plt.ylabel(receta.valores_calculo.get(nombre_valor, "Unidades"))
                plt.show()