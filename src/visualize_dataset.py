# src/visualize_dataset.py

import pandas as pd
from ucimlrepo import fetch_ucirepo

def load_and_prepare_data():
    # Carregar o dataset Breast Cancer Wisconsin (Diagnostic) usando seu ID no UCI
    dataset = fetch_ucirepo(id=17)
    
    # Extrair as features e os targets
    X = dataset.data.features
    y = dataset.data.targets
    
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
    
    return dataset, data

def display_dataset_info(dataset, data):
    # Exibir informações das colunas
    print("Informações das Colunas:")
    print(dataset.variables)
    print("\n")

    # Calcular o número de linhas
    num_linhas = len(data)
    print(f"Número de linhas no dataset: {num_linhas}")

    if num_linhas > 2000:
        print("Alerta: O dataset possui mais de 2000 linhas.")
        print("Exibindo as 10 primeiras linhas:")
        print(data.head(10))
        
    else:
        print("Exibindo todas as linhas do dataset:")
        print(data.columns)
        print(data)
    
def salvar_dataset(data):
    # Perguntar ao usuário se deseja salvar os dados
    salvar = input("\nDeseja salvar o dataset em um arquivo CSV? (s/n): ").strip().lower()
    if salvar == 's':
        caminho = input("Digite o caminho para salvar o arquivo (ex: data/output.csv): ").strip()
        try:
            data.to_csv(caminho, index=False)
            print(f"Dataset salvo com sucesso em {caminho}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
    else:
        print("Operação de salvamento cancelada.")

def main():
    dataset, data = load_and_prepare_data()
    display_dataset_info(dataset, data)
    salvar_dataset(data)

if __name__ == "__main__":
    main()
