import streamlit as st
import pandas as pd
import os

FILE_PATH = "nf_registro.xlsx"

# Função para carregar os dados existentes ou criar uma nova planilha
# Função para carregar os dados existentes ou criar uma nova planilha
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        # Garantir que a coluna "Valor" seja do tipo float
        df["Valor"] = df["Valor"].astype(float)
        return df
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
    ("Cadastro de NF","Editar NF", "Consulta de NF"),  # Adiciona "Editar NF"
    index=0,
    format_func=lambda x: f"📝 {x}" if x == "Cadastro de NF" else f"🔍 {x}" if x == "Consulta de NF" else f"✏️ {x}",
    horizontal=True
)

# Se o usuário escolher "Editar NF"
if menu == "Editar NF":
    st.header("Editar Notas Fiscais")

    # Carregar os dados
    df = load_data()

    # Campo de busca para escolher a NF que deseja editar
    nf_selecionada = st.selectbox(
        "Qual NF você quer editar?",
        options=["Selecione..."] + list(df["Número NF"].unique())  # Adiciona a opção de selecionar uma NF
    )

    if nf_selecionada != "Selecione...":
        # Filtrar a NF selecionada
        nf_data = df[df["Número NF"] == nf_selecionada].iloc[0]

        # Exibir os campos de cadastro com os dados atuais da NF
        txt_numero_nf = st.text_input("Número da NF", value=nf_data["Número NF"], disabled=True)
        date_data = st.date_input("Data da NF", value=pd.to_datetime(nf_data["Data"]))
        txt_valor = st.number_input("Valor", min_value=0.0, format="%.2f", value=nf_data["Valor"])
        txt_fornecedor = st.text_input("Fornecedor", value=nf_data["Fornecedor"])
        txt_descricao = st.text_area("Descrição", value=nf_data["Descrição"])

        # Botão de salvar
        if st.button("Salvar Alterações"):
            # Atualiza os dados da NF selecionada
            df.loc[df["Número NF"] == nf_selecionada, ["Data", "Valor", "Fornecedor", "Descrição"]] = [date_data, txt_valor, txt_fornecedor, txt_descricao]

            # Salvar as alterações no arquivo Excel
            save_data(df)

            st.success("Nota Fiscal editada com sucesso!")

# Se o usuário escolher "Cadastro de NF"
if menu == "Cadastro de NF":
    st.header("Cadastro de Notas Fiscais")
    
    import locale
   


    df = load_data()

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


        # Lista de fornecedores já cadastrados no DataFrame
    fornecedores_existentes = df["Fornecedor"].unique().tolist()

    # Adicionando uma opção para o usuário adicionar um novo fornecedor
    fornecedor_opcao = st.selectbox(
        "Fornecedor", 
        options=["Novo fornecedor..."] + fornecedores_existentes,  # A PRIMEIRA opção será para novo fornecedor
        index=1
    )

    # Caso o usuário queira adicionar um novo fornecedor
    if fornecedor_opcao == "Novo fornecedor...":
        txt_fornecedor = st.text_input("Digite o nome do novo fornecedor")
    else:
        txt_fornecedor = fornecedor_opcao

    # Campos de entrada para o cadastro
    txt_numero_nf = st.text_input("Número da NF", value=st.session_state.txt_numero_nf)
    date_data = st.date_input("Data da NF", value=st.session_state.date_data, format="DD/MM/YYYY")
    txt_valor = st.number_input("Valor (R$)", value = st.session_state.txt_valor)

    
    
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
    nota_filtrar = st.sidebar.multiselect(
        "Número NF",
        options=list(df["Número NF"].unique()),  # Remove a opção "Todos"
        default=[]  # Filtro vazio por padrão, ou seja, nada selecionado inicialmente
    )

    # Filtros
    fornecedor_filtrar = st.sidebar.multiselect(
        "Fornecedor",
        options=list(df["Fornecedor"].unique()),  # Remove a opção "Todos"
        default=[]  # Filtro vazio por padrão, ou seja, nada selecionado inicialmente
    )


    # Se nenhum fornecedor for selecionado, incluir todos os fornecedores
    if not fornecedor_filtrar:
        fornecedor_filtrar = df["Fornecedor"].unique()

    # Se nenhum número de NF for selecionado, incluir todos os números de NF
    if not nota_filtrar:
        nota_filtrar = df["Número NF"].unique()



    data_inicio = st.sidebar.date_input("Data Início", df["Data"].min(), format="DD/MM/YYYY")
    data_fim = st.sidebar.date_input("Data Fim", df["Data"].max(), format="DD/MM/YYYY")

    # Aplicar filtros
    df_filtrado = df[
        (df["Fornecedor"].isin(fornecedor_filtrar)) &
        (df["Data"] >= pd.to_datetime(data_inicio)) &
        (df["Data"] <= pd.to_datetime(data_fim)) &
        (df["Número NF"].isin(nota_filtrar))
    ]



    # Exibir os registros filtrados
    df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"]).dt.strftime("%d/%m/%Y")  # Formatar data no formato BR
    # Calcular a altura da tabela com base no número de linhas
    num_linhas = len(df)
    altura = min(num_linhas * 30, 600)  # Cada linha com altura de 30px, ajustável. Limite em 600px.

    st.dataframe(df_filtrado, height=altura, use_container_width=True)
    
