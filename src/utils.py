# src/utils.py

import pandas as pd
from ucimlrepo import fetch_ucirepo

def load_data():
    """
    Carrega o conjunto de dados Breast Cancer Wisconsin (Diagnostic) da UCI Machine Learning Repository.
    
    :return: DataFrame contendo os dados com colunas renomeadas e um ID sequencial.
    """
    # Buscar o dataset Breast Cancer Wisconsin (Diagnostic) usando o ID da UCI
    breast_cancer_wisconsin_diagnostic = fetch_ucirepo(id=17)
    
    # Extrair as features e os targets
    X = breast_cancer_wisconsin_diagnostic.data.features
    y = breast_cancer_wisconsin_diagnostic.data.targets
    
    # Combinar features e targets em um único DataFrame
    data = X.copy()
    data['Diagnosis'] = y['Diagnosis']
    data['ID'] = range(1, len(data) + 1)  # Criar um ID sequencial
    
    # Reorganizar as colunas para ter ID e Diagnosis primeiro
    cols = ['ID', 'Diagnosis'] + [col for col in data.columns if col not in ['ID', 'Diagnosis']]
    data = data[cols]
    
    # Renomear as colunas para corresponder aos nomes esperados
    base_features = [
        'radius', 'texture', 'perimeter', 'area', 'smoothness',
        'compactness', 'concavity', 'concave_points', 'symmetry', 'fractal_dimension'
    ]
    suffixes = {1: 'mean', 2: 'se', 3: 'worst'}
    new_columns = {}
    
    for feature in base_features:
        for i in [1, 2, 3]:
            old_name = f'{feature}{i}'
            new_name = f'{feature.capitalize()}_{suffixes[i]}'
            new_columns[old_name] = new_name
    
    data = data.rename(columns=new_columns)
    
    return data

def normalize_data(dataframe, entrada):
    """
    Normaliza os atributos de entrada utilizando Min-Max Scaling baseado nos valores da base de dados.
    
    :param dataframe: DataFrame contendo os dados da base.
    :param entrada: Dicionário de atributos e seus respectivos valores de entrada.
    :return: Dicionário de atributos normalizados.
    """
    normalized = {}
    for attr, val in entrada.items():
        min_val = dataframe[attr].min()
        max_val = dataframe[attr].max()
        if max_val - min_val != 0:
            normalized_val = (val - min_val) / (max_val - min_val)
        else:
            normalized_val = 0.0  # Evita divisão por zero se todos os valores forem iguais
        normalized[attr] = normalized_val
    return normalized

def zscore_normalize(dataframe, entrada):
    """
    Normaliza os atributos de entrada utilizando Z-Score Standardization baseado nos valores da base de dados.
    
    :param dataframe: DataFrame contendo os dados da base.
    :param entrada: Dicionário de atributos e seus respectivos valores de entrada.
    :return: Dicionário de atributos normalizados.
    """
    normalized = {}
    for attr, val in entrada.items():
        mean_val = dataframe[attr].mean()
        std_val = dataframe[attr].std()
        if std_val != 0:
            normalized_val = (val - mean_val) / std_val
        else:
            normalized_val = 0.0  # Evita divisão por zero se o desvio padrão for zero
        normalized[attr] = normalized_val
    return normalized
