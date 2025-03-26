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
st.title("Cadastro e Consulta de Notas Fiscais")

# Usar CSS para centralizar "Escolha a opção" na página
st.markdown("""
    <style>
        /* Centraliza o texto "Escolha a opção" */
        .centralizado {
            display: flex;
            justify-content: center;
            text-align: center;
            font-size: 15px;
            margin-bottom: 10px;
        }

        /* Centraliza as opções do radio */
        .stRadio {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Título "Escolha a opção" centralizado
st.markdown('<div class="centralizado">Escolha a opção</div>', unsafe_allow_html=True)

# Criando as abas de navegação com ícones e layout horizontal
menu = st.radio(
    "",
    ("Cadastro de NF", "Consulta de NF"),
    index=0,  # Deixa "Cadastro de NF" como opção inicial
    format_func=lambda x: f"📝 {x}" if x == "Cadastro de NF" else f"🔍 {x}",
    horizontal=True
)

# Se o usuário escolher "Cadastro de NF"
if menu == "Cadastro de NF":
    st.header("Cadastro de Notas Fiscais")

    # Campos de entrada com controle de session_state
    if "txt_numero_nf" not in st.session_state:
        st.session_state.txt_numero_nf = ""
    if "date_data" not in st.session_state:
        st.session_state.date_data = None
    if "txt_valor" not in st.session_state:
        st.session_state.txt_valor = 0.0
    if "txt_fornecedor" not in st.session_state:
        st.session_state.txt_fornecedor = ""
    if "txt_descricao" not in st.session_state:
        st.session_state.txt_descricao = ""

    # Campos de entrada para o cadastro
    txt_numero_nf = st.text_input("Número da NF", value=st.session_state.txt_numero_nf)
    date_data = st.date_input("Data da NF", value=st.session_state.date_data, format="DD/MM/YYYY")
    txt_valor = st.number_input("Valor", min_value=0.0, format="%.2f", value=st.session_state.txt_valor)
    txt_fornecedor = st.text_input("Fornecedor", value=st.session_state.txt_fornecedor)
    txt_descricao = st.text_area("Descrição", value=st.session_state.txt_descricao)

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

                # Resetar os campos de input para os valores padrão
                st.session_state.txt_numero_nf = ""
                st.session_state.date_data = None
                st.session_state.txt_valor = 0.0
                st.session_state.txt_fornecedor = ""
                st.session_state.txt_descricao = ""

        else:
            st.error("Preencha os campos obrigatórios: Número NF e Fornecedor.")

# Se o usuário escolher "Consulta de NF"
elif menu == "Consulta de NF":
    st.header("Consulta de Notas Fiscais")

    # Barra lateral para filtros
    st.sidebar.header("Filtros")

    # Carregar os dados
    df = load_data()

    # Filtros
    fornecedor_filtrar = st.sidebar.multiselect(
        "Fornecedor",
        options=["Todos"] + list(df["Fornecedor"].unique()),  # Adiciona "Todos" como primeira opção
        default=["Todos"]  # O valor padrão é "Todos"
    )

    # Se "Todos" for selecionado, incluir todos os fornecedores
    if "Todos" in fornecedor_filtrar:
        fornecedor_filtrar = df["Fornecedor"].unique()

    data_inicio = st.sidebar.date_input("Data Início", df["Data"].min(), format="DD/MM/YYYY")
    data_fim = st.sidebar.date_input("Data Fim", df["Data"].max(), format="DD/MM/YYYY")

    # Aplicar filtros
    df_filtrado = df[
        (df["Fornecedor"].isin(fornecedor_filtrar)) &
        (df["Data"] >= pd.to_datetime(data_inicio)) &
        (df["Data"] <= pd.to_datetime(data_fim))
    ]



    # Exibir os registros filtrados
    df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"]).dt.strftime("%d/%m/%Y")  # Formatar data no formato BR
    # Calcular a altura da tabela com base no número de linhas
    num_linhas = len(df)
    altura = min(num_linhas * 30, 600)  # Cada linha com altura de 30px, ajustável. Limite em 600px.

    st.dataframe(df_filtrado, height=altura, use_container_width=True)
    
