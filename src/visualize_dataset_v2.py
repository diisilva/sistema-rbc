# src/visualize_dataset.py

import pandas as pd
from ucimlrepo import fetch_ucirepo
import openpyxl

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

def extract_column_descriptions(dataset, data):
    """
    Extrai as descrições das colunas a partir do campo 'variable_info' do metadata.
    Retorna um DataFrame com as informações.
    """
    variable_info_text = dataset.metadata.additional_info.variable_info
    
    # Inicializar dicionários para armazenar descrições
    descriptions = {}
    
    # Separar as linhas do texto
    linhas = variable_info_text.split('\n')
    
    # Processar as descrições básicas
    for linha in linhas:
        if linha.startswith('1) ID number'):
            descriptions['ID'] = 'Identificador único da amostra.'
        elif linha.startswith('2) Diagnosis'):
            descriptions['Diagnosis'] = 'Diagnóstico da amostra (M = Maligno, B = Benigno).'
        elif 'Ten real-valued features are computed for each cell nucleus' in linha:
            # Início das descrições das features
            continue
        elif any(linha.startswith(f"{chr(97 + i)}) ") for i in range(10)):
            # Descrições das features a-j
            parte = linha.split(')', 1)
            if len(parte) == 2:
                feature_letter = parte[0].strip()
                feature_desc = parte[1].strip()
                feature_map = {
                    'a': 'Radius',
                    'b': 'Texture',
                    'c': 'Perimeter',
                    'd': 'Area',
                    'e': 'Smoothness',
                    'f': 'Compactness',
                    'g': 'Concavity',
                    'h': 'Concave_points',
                    'i': 'Symmetry',
                    'j': 'Fractal_dimension'
                }
                feature_name = feature_map.get(feature_letter.lower())
                if feature_name:
                    descriptions[feature_name] = feature_desc
    
    # Adicionar descrições para as variações (mean, se, worst)
    columns_info = {
        'ID': {'role': 'ID', 'type': 'Categorical'},
        'Diagnosis': {'role': 'Target', 'type': 'Categorical'}
    }
    
    base_features = [
        'Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness',
        'Compactness', 'Concavity', 'Concave_points', 'Symmetry', 'Fractal_dimension'
    ]
    variations = ['mean', 'se', 'worst']
    
    # Descrições em inglês
    descriptions_en = {
        'Radius': 'Mean of distances from center to points on the perimeter.',
        'Texture': 'Standard deviation of gray-scale values.',
        'Perimeter': 'Mean perimeter of the cell nuclei.',
        'Area': 'Mean area of the cell nuclei.',
        'Smoothness': 'Local variation in radius lengths.',
        'Compactness': 'Perimeter^2 / area - 1.0.',
        'Concavity': 'Severity of concave portions of the contour.',
        'Concave_points': 'Number of concave portions of the contour.',
        'Symmetry': 'Symmetry of the cell nuclei.',
        'Fractal_dimension': 'Fractal dimension ("coastline approximation" - 1).'
    }
    
    # Descrições em português
    descriptions_pt = {
        'Radius': 'Média das distâncias do centro até os pontos na perímetro.',
        'Texture': 'Desvio padrão dos valores em escala de cinza.',
        'Perimeter': 'Média do perímetro dos núcleos celulares.',
        'Area': 'Média da área dos núcleos celulares.',
        'Smoothness': 'Variação local nos comprimentos dos raios.',
        'Compactness': 'Perímetro^2 / área - 1.0.',
        'Concavity': 'Gravidade das porções côncavas do contorno.',
        'Concave_points': 'Número de porções côncavas do contorno.',
        'Symmetry': 'Simetria dos núcleos celulares.',
        'Fractal_dimension': 'Dimensão fractal ("aproximação da costa" - 1).'
    }
    
    for feature in base_features:
        for var in variations:
            col_name = f'{feature}_{var}'
            if var == 'mean':
                desc_en = descriptions_en.get(feature, 'Description not available.')
                desc_pt = descriptions_pt.get(feature, 'Descrição não disponível.')
            elif var == 'se':
                desc_en = f'Standard error of {descriptions_en.get(feature, "description").lower()}'
                desc_pt = f'Erro padrão de {descriptions_pt.get(feature, "descrição").lower()}'
            elif var == 'worst':
                desc_en = f'Worst case of {descriptions_en.get(feature, "description").lower()}'
                desc_pt = f'Melhor caso de {descriptions_pt.get(feature, "descrição").lower()}'
            columns_info[col_name] = {
                'role': 'Feature',
                'type': 'Continuous',
                'description_en': desc_en,
                'description_pt': desc_pt
            }
    
    # Criar DataFrame das informações das colunas
    columns_df = pd.DataFrame([
        {'name': name,
         'role': info['role'],
         'type': info['type'],
         'description_en': info.get('description_en', 'Description not available.'),
         'description_pt': info.get('description_pt', 'Descrição não disponível.')}
        for name, info in columns_info.items()
    ])
    
    # Obter os tipos de dados reais do DataFrame
    data_dtypes = data.dtypes.apply(lambda x: map_pandas_dtype(x)).to_dict()
    
    # Adicionar a coluna 'Data Type' ao DataFrame de descrições
    columns_df['Data Type'] = columns_df['name'].map(data_dtypes)
    
    return columns_df

def map_pandas_dtype(dtype):
    """
    Mapeia os tipos de dados do pandas para tipos mais legíveis.
    """
    if pd.api.types.is_string_dtype(dtype):
        return 'String'
    elif pd.api.types.is_integer_dtype(dtype):
        return 'Integer'
    elif pd.api.types.is_float_dtype(dtype):
        return 'Float'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'Boolean'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DateTime'
    else:
        return 'Other'

def display_dataset_info(dataset, data, columns_df):
    # Exibir informações das colunas
    print("Informações das Colunas:")
    print(columns_df)
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
        print(data)

def salvar_dataset_em_xlsx(dataset, data, columns_df):
    # Perguntar ao usuário se deseja salvar os dados
    salvar = input("\nDeseja salvar o dataset em um arquivo Excel (.xlsx)? (s/n): ").strip().lower()
    if salvar == 's':
        caminho = input("Digite o caminho completo para salvar o arquivo (ex: C:/Users/SeuUsuario/Downloads/output.xlsx): ").strip()
        try:
            with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
                # Salvar os dados
                data.to_excel(writer, sheet_name='Dados', index=False)
                
                # Salvar as informações das colunas com uma coluna adicional para descrição da coluna original
                informacoes_colunas = pd.DataFrame(dataset.variables)
                informacoes_colunas['Descrição da Coluna'] = informacoes_colunas['name'].map(lambda x: map_coluna_descricao(x))
                informacoes_colunas.to_excel(writer, sheet_name='Informações das Colunas', index=False)
                
                # Salvar a descrição detalhada das colunas
                columns_df_selected = columns_df[
                    ['name', 'Data Type', 'description_en', 'description_pt']
                ]
                columns_df_selected = columns_df_selected.rename(columns={
                    'name': 'Column Name',
                    'Data Type': 'Data Type',
                    'description_en': 'Description (EN)',
                    'description_pt': 'Descrição (PT)'
                })
                columns_df_selected.to_excel(writer, sheet_name='Descrição das Colunas', index=False)
            
            print(f"Dataset salvo com sucesso em {caminho}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
    else:
        print("Operação de salvamento cancelada.")

def map_coluna_descricao(name):
    """
    Mapeia o nome original da coluna para sua descrição em português.
    """
    descricao_map = {
        'radius1': 'Radius_mean: Média dos raios das células.',
        'texture1': 'Texture_mean: Média da textura das células.',
        'perimeter1': 'Perimeter_mean: Média do perímetro das células.',
        'area1': 'Area_mean: Média da área das células.',
        'smoothness1': 'Smoothness_mean: Média da suavidade das células.',
        'compactness1': 'Compactness_mean: Média da compactação das células.',
        'concavity1': 'Concavity_mean: Média da concavidade das células.',
        'concave_points1': 'Concave_points_mean: Média dos pontos côncavos das células.',
        'symmetry1': 'Symmetry_mean: Média da simetria das células.',
        'fractal_dimension1': 'Fractal_dimension_mean: Média da dimensão fractal das células.',
        'radius2': 'Radius_se: Erro padrão da média dos raios das células.',
        'texture2': 'Texture_se: Erro padrão da média da textura das células.',
        'perimeter2': 'Perimeter_se: Erro padrão da média do perímetro das células.',
        'area2': 'Area_se: Erro padrão da média da área das células.',
        'smoothness2': 'Smoothness_se: Erro padrão da média da suavidade das células.',
        'compactness2': 'Compactness_se: Erro padrão da média da compactação das células.',
        'concavity2': 'Concavity_se: Erro padrão da média da concavidade das células.',
        'concave_points2': 'Concave_points_se: Erro padrão da média dos pontos côncavos das células.',
        'symmetry2': 'Symmetry_se: Erro padrão da média da simetria das células.',
        'fractal_dimension2': 'Fractal_dimension_se: Erro padrão da média da dimensão fractal das células.',
        'radius3': 'Radius_worst: Valor pior do raio das células.',
        'texture3': 'Texture_worst: Valor pior da textura das células.',
        'perimeter3': 'Perimeter_worst: Valor pior do perímetro das células.',
        'area3': 'Area_worst: Valor pior da área das células.',
        'smoothness3': 'Smoothness_worst: Valor pior da suavidade das células.',
        'compactness3': 'Compactness_worst: Valor pior da compactação das células.',
        'concavity3': 'Concavity_worst: Valor pior da concavidade das células.',
        'concave_points3': 'Concave_points_worst: Valor pior dos pontos côncavos das células.',
        'symmetry3': 'Symmetry_worst: Valor pior da simetria das células.',
        'fractal_dimension3': 'Fractal_dimension_worst: Valor pior da dimensão fractal das células.'
    }
    return descricao_map.get(name, 'Descrição não disponível.')

def main():
    dataset, data = load_and_prepare_data()
    columns_df = extract_column_descriptions(dataset, data)
    display_dataset_info(dataset, data, columns_df)
    salvar_dataset_em_xlsx(dataset, data, columns_df)

if __name__ == "__main__":
    main()
