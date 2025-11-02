import os
import pandas as pd

FILE_PATH = "data/nf_registro.xlsx"

# Definir as colunas necessárias
required_columns = [
    "Número NF", "Data", "Valor", "Fornecedor", "Descrição",
    "Projeto", "Tipo", "Produto", "Descrição do item", "Mês contratado", 
    "Modelo de Contrato", "Data de faturamento NF", 
    "Data Recebimento NF", "Data de lançamento NF", "Validação Financeiro",
    "Mês Planilha Financeiro", "Observações"
]

# Função para salvar os dados no Excel
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Função para carregar os dados existentes ou criar uma nova planilha
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        # Garantir que as colunas numéricas sejam do tipo correto
        df["Valor"] = df["Valor"].astype(int)
        # Verifica se todas as colunas necessárias estão presentes, caso contrário, cria-las
        for col in required_columns:
            if col not in df.columns:
                df[col] = None  # Adiciona as colunas ausentes
        return df
    else:
        # Se o arquivo não existir, cria um novo DataFrame com as colunas necessárias
        df = pd.DataFrame(columns=required_columns)
        # Salvar a nova planilha vazia no disco
        save_data(df)
        return df
