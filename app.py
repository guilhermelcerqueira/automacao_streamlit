# %%
import streamlit as st
import pandas as pd
import os

FILE_PATH = "nf_registro.xlsx"

# Função para carregar os dados existentes ou criar uma nova planilha
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    return pd.DataFrame(columns=["Número NF", "Data", "Valor", "Fornecedor", "Descrição"])

# Função para salvar os dados no Excel
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Título da aplicação
st.title("Cadastro de Notas Fiscais")

# Campos de entrada
txt_numero_nf = st.text_input("Número da NF")
date_data = st.date_input("Data da NF")
txt_valor = st.number_input("Valor", min_value=0.0, format="%.2f")
txt_fornecedor = st.text_input("Fornecedor")
txt_descricao = st.text_area("Descrição")

# Botão de salvar
if st.button("Salvar"):
    if txt_numero_nf and txt_fornecedor:
        df = load_data()
        
        # Verificar se NF já existe
        if txt_numero_nf in df["Número NF"].values:
            st.warning("Essa NF já foi cadastrada!")
        else:
            novo_registro = pd.DataFrame({
                "Número NF": [txt_numero_nf],
                "Data": [date_data],
                "Valor": [txt_valor],
                "Fornecedor": [txt_fornecedor],
                "Descrição": [txt_descricao]
            })
            df = pd.concat([df, novo_registro], ignore_index=True)
            save_data(df)
            st.success("Nota Fiscal cadastrada com sucesso!")
    else:
        st.error("Preencha os campos obrigatórios: Número NF e Fornecedor.")

# Exibir os registros cadastrados
st.subheader("Registros Cadastrados")
df = load_data()
st.dataframe(df)

