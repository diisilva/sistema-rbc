# src/cbr.py

import math
from src.utils import normalize_data  # Importando a função de normalização

class Caso:
    def __init__(self, id, diagnosis, atributos):
        self.id = id
        self.diagnosis = diagnosis
        self.atributos = atributos  # Dicionário de atributos e seus valores

class BaseDeCasos:
    def __init__(self, dataframe, atributos_relevantes, normalizar=False):
        """
        Inicializa a base de casos a partir de um DataFrame e uma lista de atributos relevantes.
        
        :param dataframe: DataFrame contendo os dados.
        :param atributos_relevantes: Lista de nomes de atributos a serem utilizados.
        :param normalizar: Booleano indicando se a base deve ser normalizada.
        """
        if normalizar:
            dataframe = dataframe.copy()  # Cria uma cópia para evitar modificar o original
            # Normalizar a base de dados usando Min-Max Scaling
            for attr in atributos_relevantes:
                min_val = dataframe[attr].min()
                max_val = dataframe[attr].max()
                if max_val - min_val != 0:
                    dataframe[attr] = (dataframe[attr] - min_val) / (max_val - min_val)
                else:
                    dataframe[attr] = 0.0  # Evita divisão por zero
        
        self.casos = []
        for index, row in dataframe.iterrows():
            atributos = {attr: row[attr] for attr in atributos_relevantes}
            caso = Caso(row['ID'], row['Diagnosis'], atributos)
            self.casos.append(caso)
    
    def recuperar_casos_similares(self, caso_entrada, pesos):
        """
        Recupera uma lista de casos similares ordenados por similaridade decrescente.
        
        :param caso_entrada: Objeto Caso representando o caso de entrada.
        :param pesos: Dicionário de pesos para cada atributo.
        :return: Lista de tuplas (caso, similaridade).
        """
        similaridades = []
        for caso in self.casos:
            similaridade = self.calcular_similaridade(caso_entrada, caso, pesos)
            similaridades.append((caso, similaridade))
        # Ordena por similaridade decrescente
        similaridades.sort(key=lambda x: x[1], reverse=True)
        return similaridades
    
    def calcular_similaridade(self, caso1, caso2, pesos):
        """
        Calcula a similaridade entre dois casos utilizando distância euclidiana ponderada.
        
        :param caso1: Objeto Caso representando o primeiro caso.
        :param caso2: Objeto Caso representando o segundo caso.
        :param pesos: Dicionário de pesos para cada atributo.
        :return: Valor de similaridade entre 0 e 1.
        """
        soma = 0
        for atributo in caso1.atributos:
            w = pesos.get(atributo, 1)
            soma += w * (caso1.atributos[atributo] - caso2.atributos[atributo]) ** 2
        distancia = math.sqrt(soma)
        similaridade = 1 / (1 + distancia)
        return similaridade
    
    def calcular_distancia(self, caso1, caso2, pesos):
        """
        Calcula a distância euclidiana ponderada entre dois casos.
        
        :param caso1: Objeto Caso representando o primeiro caso.
        :param caso2: Objeto Caso representando o segundo caso.
        :param pesos: Dicionário de pesos para cada atributo.
        :return: Valor da distância.
        """
        soma = 0
        for atributo in caso1.atributos:
            w = pesos.get(atributo, 1)
            soma += w * (caso1.atributos[atributo] - caso2.atributos[atributo]) ** 2
        distancia = math.sqrt(soma)
        return distancia
