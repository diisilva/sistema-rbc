
# Sistema RBC - Diagnóstico de Câncer de Mama

## Descrição

O **Sistema RBC (Raciocínio Baseado em Casos)** é uma aplicação desenvolvida em Python para auxiliar no diagnóstico de câncer de mama. Utilizando o método de **Raciocínio Baseado em Casos (CBR)**, o sistema compara as características de um novo caso inserido pelo usuário com uma base de casos previamente armazenados, classificando o tumor como Benigno (B) ou Maligno (M).

## Características

- **Aquisição de Dados:** Importa e processa o conjunto de dados Breast Cancer Wisconsin (Diagnostic) da UCI Machine Learning Repository utilizando a biblioteca `ucimlrepo`.
- **Normalização de Dados:** Opção para normalizar os dados utilizando Min-Max Scaling.
- **Interface Gráfica (GUI):** Interface amigável desenvolvida com Tkinter para inserção de casos, ajuste de pesos dos atributos e visualização de resultados.
- **Cálculo de Similaridade:** Utiliza distância Euclidiana ponderada para calcular a similaridade entre casos.
- **Exibição de Resultados:** Apresenta uma lista ordenada de casos similares com métricas detalhadas.
- **Flexibilidade:** Permite ao usuário ajustar a importância de cada atributo no cálculo de similaridade.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.x
- **Bibliotecas:**
  - `tkinter` para a interface gráfica
  - `pandas` para manipulação de dados
  - `math` para cálculos matemáticos
  - `ucimlrepo` para aquisição de dados da UCI Machine Learning Repository

## Instalação

### Pré-requisitos

- **Python 3.x** instalado em sua máquina.
- **Bibliotecas Python:** As seguintes bibliotecas devem estar instaladas. Você pode instalá-las utilizando o `pip`.

### Passos para Instalação

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/diisilva/sistema-rbc.git
   ```
   
2. **Navegue até o Diretório do Projeto:**
   ```bash
   cd sistema-rbc
   ```
   
3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

   Caso não exista um arquivo requirements.txt, instale as bibliotecas manualmente:
   ```bash
   pip install pandas tkinter ucimlrepo
   ```

## Uso

### Execute o Programa:
   ```bash
   python -m gui.interface
   ```

### Interface do Usuário:

- **Inserção de Caso:** Preencha os valores dos atributos do caso de entrada ou utilize os botões para pré-preencher com médias ou medianas de casos Benignos (B) ou Malignos (M).
- **Ajuste de Pesos:** Modifique os pesos dos atributos conforme a importância desejada para o cálculo de similaridade.
- **Normalização:** Ative ou desative a normalização dos dados utilizando o checkbox "Normalizar Dados".
- **Buscar Casos Similares:** Clique em "Buscar Casos Similares" para visualizar uma lista ordenada de casos similares da base.
- **Limpar Resultados:** Utilize o botão "Limpar Resultados" para resetar as entradas e resultados exibidos.
- **Sobre:** Acesse informações detalhadas sobre o sistema através do botão "Sobre".

### Interpretação dos Resultados:

- **Caso de Entrada:** Valores dos atributos inseridos pelo usuário.
- **Pesos Atribuídos:** Importância definida para cada atributo.
- **Lista de Casos Similares:** Casos da base ordenados por similaridade, exibindo ID, Diagnóstico, Similaridade (%), Similarity Score e Distance Metrics.

## Estrutura do Projeto

```
sistema-rbc/
├── gui/
│   └── interface.py         # Interface gráfica do usuário
├── src/
│   ├── cbr.py               # Lógica de Raciocínio Baseado em Casos
│   └── utils.py             # Utilitários para carregamento e normalização de dados
```

## Modelagem

### Atributos Utilizados

O sistema utiliza 30 atributos numéricos computados a partir de imagens digitalizadas de aspirações por agulha fina (FNA) de massas mamárias. Estes atributos descrevem características dos núcleos celulares, tais como:

#### Medidas de Tendência Central:
- Radius_mean, Texture_mean, Perimeter_mean, Area_mean, Smoothness_mean, Compactness_mean, Concavity_mean, Concave_points_mean, Symmetry_mean, Fractal_dimension_mean

#### Medidas de Variabilidade:
- Radius_se, Texture_se, Perimeter_se, Area_se, Smoothness_se, Compactness_se, Concavity_se, Concave_points_se, Symmetry_se, Fractal_dimension_se

#### Medidas de Máxima Variedade:
- Radius_worst, Texture_worst, Perimeter_worst, Area_worst, Smoothness_worst, Compactness_worst, Concavity_worst, Concave_points_worst, Symmetry_worst, Fractal_dimension_worst

### Métrica de Similaridade

Distância Euclidiana Ponderada:
```
Distância = sqrt(Σ w_i * (entrada_i - caso_i)^2)
```
Onde:
- Pesos (w_i): Determinam a importância relativa de cada atributo na similaridade.
- Entrada (entrada_i): Valor do atributo no caso de entrada.
- Caso (caso_i): Valor do atributo no caso da base.

Similaridade = 1 / (1 + Distância)

## Resultados e Avaliação

### Exemplo de Saída

```
ID    Diagnosis  Similaridade (%)     Similarity Score     Distance Metrics
--------------------------------------------------------------------------------
442   M          4.45                 0.0445               21.4511
263   M          2.62                 0.0262               37.1375
157   M          2.03                 0.0203               48.1516
33    M          1.84                 0.0184               53.4746
445   M          1.54                 0.0154               64.0750
168   M          1.54                 0.0154               64.1004
120   M          1.49                 0.0149               66.0673
401   M          1.49                 0.0149               66.1309
336   M          1.46                 0.0146               67.4031
202   M          1.42                 0.0142               69.3686
```

#### Significado dos Campos
- **ID:** Identificador único do caso na base de dados.
- **Diagnosis:** Classificação do diagnóstico (B para Benigno, M para Maligno).
- **Similaridade (%):** Percentual que representa o grau de similaridade entre o caso de entrada e o caso da base.
- **Similarity Score:** Valor normalizado da similaridade, calculado como 1 / (1 + distância).
- **Distance Metrics:** Distância Euclidiana ponderada entre o caso de entrada e o caso da base.

## Pontos Fortes e Fracos

### Pontos Fortes

- Modularidade: Código organizado em módulos, facilitando a manutenção.
- Flexibilidade: Interface permite ajuste de pesos e inserção de novos casos.
- Eficiência: Utilização de bibliotecas otimizadas.
- Facilidade de Interpretação: Resultados apresentados de forma clara.

### Pontos Fracos

- Escalabilidade Limitada: Pode enfrentar lentidão com bases muito grandes.
- Dependência de Interface Gráfica: Limita a utilização em servidores.
- Manutenção da Base: Necessidade de garantir a normalização correta.
- Sensibilidade a Atributos Irrelevantes: Necessita cuidado na seleção dos atributos.

## Próximos Passos

- Implementação de Técnicas Avançadas como Random Forests e PCA.
- Expansão da Base de Casos.
- Integração com outras técnicas de IA, como Deep Learning.
- Avaliação em ambiente clínico.

## Conclusão

O Sistema RBC demonstra a eficácia do CBR na classificação de câncer de mama, com grande potencial de melhoria com as futuras implementações propostas.

## Referências

- **Banco de Dados:** UCI ML Repository - "Breast Cancer Wisconsin (Diagnostic)". <https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic>
- **Artigos e Métodos:** Bennett, K.P. "Decision Tree Construction Via Linear Programming", 1992. <https://minds.wisconsin.edu/bitstream/handle/1793/59692/TR1131.pdf;jsessionid=81AFB864A55407854A2D21877C67F411?sequence=1>

- **GitHub para essa base e outras diversas**
  https://github.com/uci-ml-repo/ucimlrepo
