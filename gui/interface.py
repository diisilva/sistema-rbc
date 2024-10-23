# gui/interface.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.cbr import BaseDeCasos, Caso
from src.utils import load_data, normalize_data, zscore_normalize  # Importando as funções de normalização

class CBRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema RBC - Diagnóstico de Câncer de Mama")
        self.root.geometry("1400x800")  # Aumentar o tamanho da janela para acomodar mais elementos

        # Carregar dados usando ucimlrepo
        self.data = load_data()
        atributos_relevantes = [
            'Radius_mean', 'Texture_mean', 'Perimeter_mean',
            'Area_mean', 'Smoothness_mean', 'Compactness_mean', 'Concavity_mean',
            'Concave_points_mean', 'Symmetry_mean', 'Fractal_dimension_mean',
            'Radius_se', 'Texture_se', 'Perimeter_se', 'Area_se', 'Smoothness_se',
            'Compactness_se', 'Concavity_se', 'Concave_points_se', 'Symmetry_se',
            'Fractal_dimension_se', 'Radius_worst', 'Texture_worst',
            'Perimeter_worst', 'Area_worst', 'Smoothness_worst',
            'Compactness_worst', 'Concavity_worst', 'Concave_points_worst',
            'Symmetry_worst', 'Fractal_dimension_worst',
        ]
        self.base_de_casos = BaseDeCasos(self.data, atributos_relevantes, normalizar=False)

        # Definir pesos iniciais
        self.pesos = {attr:1 for attr in atributos_relevantes}

        # Calcular valores medianos e médias para pré-preencher as entradas
        self.calcular_valores_referencia()

        # Criar widgets
        self.create_widgets(atributos_relevantes)

    def calcular_valores_referencia(self):
        # Filtrar casos Malignos e Benignos
        data_maligno = self.data[self.data['Diagnosis'] == 'M']
        data_benigno = self.data[self.data['Diagnosis'] == 'B']

        # Calcular medianas e médias apenas para atributos numéricos
        self.valores_medianos_m = data_maligno.select_dtypes(include=['float', 'int']).median().to_dict()
        self.valores_medias_m = data_maligno.select_dtypes(include=['float', 'int']).mean().to_dict()

        self.valores_medianos_b = data_benigno.select_dtypes(include=['float', 'int']).median().to_dict()
        self.valores_medias_b = data_benigno.select_dtypes(include=['float', 'int']).mean().to_dict()

    def create_widgets(self, atributos):
        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill='both', expand=True)

        # Frame para entradas de atributos e pesos
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(side='top', fill='x', padx=10, pady=5)

        # Dividir os atributos em duas listas para duas colunas
        meio = len(atributos) // 2
        atributos_col1 = atributos[:meio]
        atributos_col2 = atributos[meio:]

        # Frame para Atributos - Coluna 1
        atributos_frame1 = ttk.LabelFrame(entrada_frame, text="Atributos (Coluna 1)", padding="10")
        atributos_frame1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N)

        # Criar entradas para atributos com valores pré-preenchidos - Coluna 1
        self.entries = {}
        row = 0
        for attr in atributos_col1:
            label = ttk.Label(atributos_frame1, text=attr)
            label.grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(atributos_frame1, width=20)
            entry.grid(row=row, column=1, pady=2, padx=(5, 15))
            # Pré-preencher com valor mediano
            entry.insert(0, f"{self.valores_medianos_m.get(attr, 0):.2f}")
            self.entries[attr] = entry
            row +=1

        # Frame para Atributos - Coluna 2
        atributos_frame2 = ttk.LabelFrame(entrada_frame, text="Atributos (Coluna 2)", padding="10")
        atributos_frame2.grid(row=0, column=1, padx=10, pady=5, sticky=tk.N)

        # Criar entradas para atributos com valores pré-preenchidos - Coluna 2
        row = 0
        for attr in atributos_col2:
            label = ttk.Label(atributos_frame2, text=attr)
            label.grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(atributos_frame2, width=20)
            entry.grid(row=row, column=1, pady=2, padx=(5, 15))
            # Pré-preencher com valor mediano
            entry.insert(0, f"{self.valores_medianos_m.get(attr, 0):.2f}")
            self.entries[attr] = entry
            row +=1

        # Separador vertical
        separator = ttk.Separator(entrada_frame, orient='vertical')
        separator.grid(row=0, column=2, sticky='ns', padx=10, pady=5)

        # Dividir os pesos em duas listas para duas colunas
        pesos_col1 = atributos_col1
        pesos_col2 = atributos_col2

        # Frame para Pesos - Coluna 1
        pesos_frame1 = ttk.LabelFrame(entrada_frame, text="Pesos (Coluna 1)", padding="10")
        pesos_frame1.grid(row=0, column=3, padx=10, pady=5, sticky=tk.N)

        # Criar entradas para pesos com valores pré-definidos - Coluna 1
        self.weight_vars = {}
        row_w = 0
        for attr in pesos_col1:
            label = ttk.Label(pesos_frame1, text=attr)
            label.grid(row=row_w, column=0, sticky=tk.W, pady=2)
            var = tk.DoubleVar(value=1.0)
            entry = ttk.Entry(pesos_frame1, textvariable=var, width=7)
            entry.grid(row=row_w, column=1, pady=2, padx=(5, 15))
            self.weight_vars[attr] = var
            row_w +=1

        # Frame para Pesos - Coluna 2
        pesos_frame2 = ttk.LabelFrame(entrada_frame, text="Pesos (Coluna 2)", padding="10")
        pesos_frame2.grid(row=0, column=4, padx=10, pady=5, sticky=tk.N)

        # Criar entradas para pesos com valores pré-definidos - Coluna 2
        row_w = 0
        for attr in pesos_col2:
            label = ttk.Label(pesos_frame2, text=attr)
            label.grid(row=row_w, column=0, sticky=tk.W, pady=2)
            var = tk.DoubleVar(value=1.0)
            entry = ttk.Entry(pesos_frame2, textvariable=var, width=7)
            entry.grid(row=row_w, column=1, pady=2, padx=(5, 15))
            self.weight_vars[attr] = var
            row_w +=1

        # Frame para os botões de atribuição
        atribuir_frame = ttk.Frame(entrada_frame)
        atribuir_frame.grid(row=0, column=5, padx=10, pady=5, sticky=tk.N)

        # Botões de Atribuição
        atribuir_media_m_btn = ttk.Button(atribuir_frame, text="Atribuir Média M", command=self.atribuir_media_m)
        atribuir_media_m_btn.pack(fill='x', pady=2)

        atribuir_mediana_m_btn = ttk.Button(atribuir_frame, text="Atribuir Mediana M", command=self.atribuir_mediana_m)
        atribuir_mediana_m_btn.pack(fill='x', pady=2)

        atribuir_media_b_btn = ttk.Button(atribuir_frame, text="Atribuir Média B", command=self.atribuir_media_b)
        atribuir_media_b_btn.pack(fill='x', pady=2)

        atribuir_mediana_b_btn = ttk.Button(atribuir_frame, text="Atribuir Mediana B", command=self.atribuir_mediana_b)
        atribuir_mediana_b_btn.pack(fill='x', pady=2)

        # Frame para opções adicionais
        opcoes_frame = ttk.Frame(entrada_frame)
        opcoes_frame.grid(row=1, column=0, columnspan=6, pady=10)

        # Variável para checkbox de normalização
        self.normalizar_var = tk.BooleanVar(value=False)  # Inicialmente desativado

        # Checkbox para normalização
        normalizar_cb = ttk.Checkbutton(opcoes_frame, text="Normalizar Dados", variable=self.normalizar_var, command=self.atualizar_normalizacao)
        normalizar_cb.pack(side='left', padx=5)

        # Botões de Busca, Limpar e Sobre
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(side='top', fill='x', padx=10, pady=5)

        buscar_btn = ttk.Button(botoes_frame, text="Buscar Casos Similares", command=self.buscar)
        buscar_btn.pack(side='left', padx=5)

        limpar_btn = ttk.Button(botoes_frame, text="Limpar Resultados", command=self.limpar)
        limpar_btn.pack(side='left', padx=5)

        sobre_btn = ttk.Button(botoes_frame, text="Sobre", command=self.sobre)
        sobre_btn.pack(side='left', padx=5)

        # Frame para resultados com scrollbar
        resultados_frame = ttk.Frame(frame)
        resultados_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(resultados_frame)
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(resultados_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame dentro do canvas
        self.result_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.result_frame, anchor='nw')

        # Área de texto para resultados
        self.result_text = tk.Text(self.result_frame, width=180, height=35, font=("Courier", 10))
        self.result_text.pack(side='top', fill='both', expand=True)

    # Funções para Atribuição dos Valores Padrão
    def atribuir_media_m(self):
        """Atribui as médias dos casos Malignos aos campos de entrada."""
        for attr, entry in self.entries.items():
            valor = self.valores_medias_m.get(attr, 0)
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.2f}")

    def atribuir_mediana_m(self):
        """Atribui as medianas dos casos Malignos aos campos de entrada."""
        for attr, entry in self.entries.items():
            valor = self.valores_medianos_m.get(attr, 0)
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.2f}")

    def atribuir_media_b(self):
        """Atribui as médias dos casos Benignos aos campos de entrada."""
        for attr, entry in self.entries.items():
            valor = self.valores_medias_b.get(attr, 0)
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.2f}")

    def atribuir_mediana_b(self):
        """Atribui as medianas dos casos Benignos aos campos de entrada."""
        for attr, entry in self.entries.items():
            valor = self.valores_medianos_b.get(attr, 0)
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.2f}")

    def atualizar_normalizacao(self):
        """
        Atualiza a base de casos aplicando ou removendo a normalização conforme a checkbox.
        """
        # Recarregar a base de casos com ou sem normalização
        atributos_relevantes = [
            'Radius_mean', 'Texture_mean', 'Perimeter_mean',
            'Area_mean', 'Smoothness_mean', 'Compactness_mean', 'Concavity_mean',
            'Concave_points_mean', 'Symmetry_mean', 'Fractal_dimension_mean',
            'Radius_se', 'Texture_se', 'Perimeter_se', 'Area_se', 'Smoothness_se',
            'Compactness_se', 'Concavity_se', 'Concave_points_se', 'Symmetry_se',
            'Fractal_dimension_se', 'Radius_worst', 'Texture_worst',
            'Perimeter_worst', 'Area_worst', 'Smoothness_worst',
            'Compactness_worst', 'Concavity_worst', 'Concave_points_worst',
            'Symmetry_worst', 'Fractal_dimension_worst',
        ]
        normalizar = self.normalizar_var.get()
        self.base_de_casos = BaseDeCasos(self.data, atributos_relevantes, normalizar=normalizar)

        # Recalcular as medianas e médias com base nos dados normalizados ou não
        self.calcular_valores_referencia()

        # Resetar as entradas para os valores medianos ou médios apropriados
        self.limpar()

    def buscar(self):
        # Obter caso de entrada
        atributos_entrada = {}
        try:
            for attr, entry in self.entries.items():
                val = float(entry.get())
                atributos_entrada[attr] = val
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
            return

        # Verificar se a normalização está ativada
        if self.normalizar_var.get():
            # Normalizar os dados de entrada usando Min-Max Scaling
            atributos_normalizados = normalize_data(self.data, atributos_entrada)
            
            caso_entrada = Caso("Entrada", "?", atributos_normalizados)
        else:
            # Não normalizar
            caso_entrada = Caso("Entrada", "?", atributos_entrada)

        # Obter pesos
        pesos = {}
        for attr, var in self.weight_vars.items():
            pesos[attr] = var.get()

        # Recuperar casos similares
        similaridades = self.base_de_casos.recuperar_casos_similares(caso_entrada, pesos)

        # Exibir resultados
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Caso de Entrada (Valores Normalizados):\n" if self.normalizar_var.get() else "Caso de Entrada:\n")
        for attr, val in (atributos_normalizados.items() if self.normalizar_var.get() else atributos_entrada.items()):
            self.result_text.insert(tk.END, f"  {attr}: {val:.2f}\n")
        self.result_text.insert(tk.END, "\nCasos da Base Ordenados por Similaridade:\n\n")

        # Cabeçalho dos resultados
        cabecalho = f"{'ID':<5} {'Diagnosis':<10} {'Similaridade (%)':<20} {'Similarity Score':<20} {'Distance Metrics':<25}\n"
        self.result_text.insert(tk.END, cabecalho)
        self.result_text.insert(tk.END, "-"*80 + "\n")

        # Iterar sobre todos os casos similares
        for i, (caso, sim) in enumerate(similaridades, 1):
            if i <= 10:
                # Similarity Score é o valor de similaridade
                similarity_score = sim  # Similaridade já está calculada

                # Calcular métricas de distância
                distance_metrics = self.base_de_casos.calcular_distancia(caso_entrada, caso, pesos)

                # Formatação com largura fixa
                linha = f"{caso.id:<5} {caso.diagnosis:<10} {sim*100:<20.2f} {similarity_score:<20.4f} {distance_metrics:<25.4f}\n"
                self.result_text.insert(tk.END, linha)
            else:
                # Exibir apenas ID, Diagnosis e Similaridade (%)
                linha = f"{caso.id:<5} {caso.diagnosis:<10} {sim*100:<20.2f}\n"
                self.result_text.insert(tk.END, linha)

        self.result_text.insert(tk.END, "\n")

    def limpar(self):
        # Limpar resultados
        self.result_text.delete(1.0, tk.END)
        # Resetar entradas para valores medianos ou médios apropriados
        for attr, entry in self.entries.items():
            if self.normalizar_var.get():
                # Se normalizado, use as medianas e médias normalizadas
                # Assumindo que os dados já estão normalizados na base
                entry.delete(0, tk.END)
                entry.insert(0, f"{self.valores_medianos_m.get(attr, 0):.2f}")
            else:
                # Se não normalizado, use os valores brutos
                entry.delete(0, tk.END)
                entry.insert(0, f"{self.valores_medianos_m.get(attr, 0):.2f}")
        messagebox.showinfo("Limpar", "Resultados e entradas foram limpos.")

    def sobre(self):
        # Criar uma nova janela
        sobre_win = tk.Toplevel(self.root)
        sobre_win.title("Sobre o Sistema RBC")
        sobre_win.geometry("700x600")

        # Texto informativo com formatação
        texto = (
            "Sistema RBC - Diagnóstico de Câncer de Mama\n\n"
            "**Metodologia:**\n"
            "Este sistema utiliza o método de **Raciocínio Baseado em Casos (CBR)** para diagnosticar o câncer de mama. Baseia-se na comparação entre os atributos do caso de entrada e os casos armazenados na base de casos.\n\n"
            "**Créditos:**\n"
            "Base de dados fornecida pela [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)).\n\n"
            "**Cálculo da Similaridade:**\n"
            "A similaridade entre casos é calculada utilizando a seguinte fórmula:\n\n"
            "**Similaridade = Σ (peso_i * |entrada_i - caso_i|) / Σ peso_i**\n\n"
            "Onde:\n"
            "- **peso_i**: Peso atribuído ao atributo i.\n"
            "- **entrada_i**: Valor do atributo i no caso de entrada.\n"
            "- **caso_i**: Valor do atributo i no caso da base.\n\n"
            "**Influência dos Pesos:**\n"
            "Os pesos determinam a importância relativa de cada atributo no cálculo da similaridade. Aumentar o peso de um atributo faz com que diferenças nesse atributo tenham maior impacto na similaridade final.\n\n"
            "**Direitos da Base de Dados:**\n"
            "A base de dados utilizada é de propriedade da [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php) e deve ser utilizada conforme os termos de uso estabelecidos.\n"
        )

        # Adicionar o texto em um widget Text com rolagem
        text_widget = tk.Text(sobre_win, wrap='word', padx=10, pady=10)
        text_widget.insert(tk.END, texto)
        text_widget.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        # Aplicar negrito às seções específicas
        text_widget.tag_add("bold", "1.0", "1.end")  # Título
        text_widget.tag_add("bold", "3.0", "3.end")  # Metodologia
        text_widget.tag_add("bold", "6.0", "6.end")  # Créditos
        text_widget.tag_add("bold", "9.0", "9.end")  # Cálculo da Similaridade
        text_widget.tag_add("bold", "14.0", "14.end")  # Influência dos Pesos
        text_widget.tag_add("bold", "19.0", "19.end")  # Direitos da Base de Dados
        text_widget.config(state='disabled')  # Tornar somente leitura
        text_widget.pack(expand=True, fill='both')

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(sobre_win, orient='vertical', command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget['yscrollcommand'] = scrollbar.set

def main():
    root = tk.Tk()
    app = CBRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
#ok