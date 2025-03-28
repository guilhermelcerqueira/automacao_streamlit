import streamlit as st
import pandas as pd
import os

FILE_PATH = "nf_registro.xlsx"

# Definir as colunas necessárias
required_columns = [
    "Número NF", "Data", "Valor", "Fornecedor", "Descrição",
    "Projeto", "Tipo", "Produto", "Descrição do item", "Mês contratado", 
    "RC, Contrato ou Direto", "Data de faturamento NF", 
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

# Título da aplicação
st.markdown("""
    <style>
        .titulo-customizado {
            font-size: 27px;  # Ajuste o tamanho conforme necessário
            font-weight: bold;
            text-align: center;
        }
    </style>
    <div class="titulo-customizado">Cadastro e Consulta de Notas Fiscais</div>
""", unsafe_allow_html=True)

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
    # Selectbox para escolher entre "Editar" ou "Excluir"
    action = st.selectbox("Escolha a ação", ["Editar", "Excluir"])
    if action == "Editar":
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
            txt_valor = st.number_input("Valor", min_value=0, value=nf_data["Valor"])
            txt_fornecedor = st.text_input("Fornecedor", value=nf_data["Fornecedor"])
            txt_descricao = st.text_area("Descrição", value=nf_data["Descrição"])

            # Adicionando os novos campos de entrada com os dados atuais da NF
            txt_projeto = st.text_input("Projeto", value=nf_data["Projeto"])
            txt_tipo = st.text_input("Tipo", value=nf_data["Tipo"])
            txt_produto = st.text_input("Produto", value=nf_data["Produto"])
            txt_desc_item = st.text_input("Descrição do item", value=nf_data["Descrição do item"])
            txt_mes_contratado = st.text_input("Mês contratado", value=nf_data["Mês contratado"])
            txt_rc_contrato = st.text_input("RC, Contrato ou Direto", value=nf_data["RC, Contrato ou Direto"])
            date_faturamento_nf = st.date_input("Data de faturamento NF", value=pd.to_datetime(nf_data["Data de faturamento NF"]))
            date_recebimento_nf = st.date_input("Data Recebimento NF", value=pd.to_datetime(nf_data["Data Recebimento NF"]))
            date_lancamento_nf = st.date_input("Data de lançamento NF", value=pd.to_datetime(nf_data["Data de lançamento NF"]))
            txt_validacao_financeiro = st.text_input("Validação Financeiro", value=nf_data["Validação Financeiro"])
            txt_mes_planilha_financeiro = st.text_input("Mês Planilha Financeiro", value=nf_data["Mês Planilha Financeiro"])
            txt_observacoes = st.text_area("Observações", value=nf_data["Observações"])

            # Botão de salvar
            # Botão de salvar
            if st.button("Salvar Alterações"):
                # Atualiza os dados da NF selecionada
                df.loc[df["Número NF"] == nf_selecionada, [
                    "Data", "Valor", "Fornecedor", "Descrição", "Projeto", "Tipo", "Produto", 
                    "Descrição do item", "Mês contratado", "RC, Contrato ou Direto", 
                    "Data de faturamento NF", "Data Recebimento NF", "Data de lançamento NF", 
                    "Validação Financeiro", "Mês Planilha Financeiro", "Observações"
                ]] = [
                    date_data, txt_valor, txt_fornecedor, txt_descricao, txt_projeto, txt_tipo, 
                    txt_produto, txt_desc_item, txt_mes_contratado, txt_rc_contrato, date_faturamento_nf, 
                    date_recebimento_nf, date_lancamento_nf, txt_validacao_financeiro, 
                    txt_mes_planilha_financeiro, txt_observacoes
                ]

                # Salvar as alterações no arquivo Excel
                save_data(df)

                st.success("Nota Fiscal editada com sucesso!")
                # Limpar campos e voltar para a tela inicial
                nf_selecionada = "Selecione..."  # Resetando o selectbox manualmente
            # Se o usuário escolher "Editar"

 # Se o usuário escolher "Excluir"
    elif action == "Excluir":
        df = load_data()
        st.header("Excluir Nota Fiscal")
        
        # Exibir a lista de NFs cadastradas para o usuário escolher
        nfs = df["Número NF"].tolist()
        nf_to_delete = st.selectbox("Escolha a NF para Excluir", nfs)
        
        # Aviso de exclusão
        st.warning(f"Atenção! A NF {nf_to_delete} será excluída permanentemente do arquivo original.")

        # Botão para confirmar a exclusão
        if st.button(f"Confirmar Exclusão da NF {nf_to_delete}"):
            # Excluir a NF selecionada
            df = df[df["Número NF"] != nf_to_delete]
            save_data(df)  # Salvar as alterações no arquivo
            st.success(f"NF {nf_to_delete} excluída com sucesso!")

# Se o usuário escolher "Cadastro de NF"
if menu == "Cadastro de NF":
    st.header("Cadastro de Notas Fiscais")
    
    import locale
   


    df = load_data()

    # Campos de entrada com controle de session_state
    if "txt_numero_nf" not in st.session_state:
        st.session_state.txt_numero_nf = 0
    if "date_data" not in st.session_state:
        st.session_state.date_data = None
    if "txt_valor" not in st.session_state:
        st.session_state.txt_valor = 0.0
    if "txt_fornecedor" not in st.session_state:
        st.session_state.txt_fornecedor = ""
    if "txt_descricao" not in st.session_state:
        st.session_state.txt_descricao = ""
    if "txt_projeto" not in st.session_state:
        st.session_state.txt_projeto = ""
    if "txt_tipo" not in st.session_state:
        st.session_state.txt_tipo = ""
    if "txt_produto" not in st.session_state:
        st.session_state.txt_produto = ""
    if "txt_desc_item" not in st.session_state:
        st.session_state.txt_desc_item = ""
    if "txt_mes_contratado" not in st.session_state:
        st.session_state.txt_mes_contratado = ""
    if "txt_rc_contrato" not in st.session_state:
        st.session_state.txt_rc_contrato = ""
    if "date_faturamento_nf" not in st.session_state:
        st.session_state.date_faturamento_nf = None
    if "date_recebimento_nf" not in st.session_state:
        st.session_state.date_recebimento_nf = None
    if "date_lancamento_nf" not in st.session_state:
        st.session_state.date_lancamento_nf = None
    if "txt_validacao_financeiro" not in st.session_state:
        st.session_state.txt_validacao_financeiro = ""
    if "txt_mes_planilha_financeiro" not in st.session_state:
        st.session_state.txt_mes_planilha_financeiro = ""
    if "txt_observacoes" not in st.session_state:
        st.session_state.txt_observacoes = ""

    txt_numero_nf = st.number_input(
        "Número da NF", 
        value=int(st.session_state.get("txt_numero_nf", 0.0))  # Garantir que seja float
    )
    # Lista de fornecedores já cadastrados no DataFrame
    fornecedores_existentes = df["Fornecedor"].unique().tolist()

    # Verifique se há fornecedores existentes
    if len(fornecedores_existentes) > 0:
        # Se houver fornecedores, coloque a opção "Novo fornecedor..." como primeira opção
        fornecedor_opcao = st.selectbox(
            "Fornecedor", 
            options=["Novo fornecedor..."] + fornecedores_existentes,  # A PRIMEIRA opção será para novo fornecedor
            index=0  # Começa com "Novo fornecedor..."
        )
    else:
        # Se não houver fornecedores cadastrados, só permita a opção de novo fornecedor
        fornecedor_opcao = st.selectbox(
            "Fornecedor", 
            options=["Novo fornecedor..."],  # Só a opção para novo fornecedor
            index=0  # Começa com a única opção disponível
        )

    # Condicional: Se a opção "Novo fornecedor..." for escolhida, exibe o campo para inserir um novo fornecedor
    if fornecedor_opcao == "Novo fornecedor...":
        novo_fornecedor = st.text_input("Digite o nome do novo fornecedor")
        if novo_fornecedor:
            st.session_state.novo_fornecedor = novo_fornecedor
            # Exibe a mensagem apenas quando o novo fornecedor for digitado
            st.write(f"Novo fornecedor adicionado: {novo_fornecedor}")
        else:
            st.session_state.novo_fornecedor = ""  # Caso o campo fique vazio
            st.write("")  # Nenhuma mensagem exibida
    else:
        # Caso um fornecedor existente seja selecionado
        novo_fornecedor = fornecedor_opcao
        st.session_state.novo_fornecedor = ""  # Não há "novo fornecedor", já foi selecionado
        # Exibe a mensagem apenas se o fornecedor for selecionado (não mais a "Novo fornecedor" texto)
        st.write(f"Fornecedor selecionado: {novo_fornecedor}")


    # Exibir o fornecedor selecionado, bloqueado para edição
    st.selectbox("Fornecedor", options=[novo_fornecedor], disabled=True)
    # Campos de entrada para o cadastro

    date_data = st.date_input("Data da NF", value=st.session_state.date_data, format="DD/MM/YYYY")
    txt_valor = st.number_input("Valor (R$)", value=st.session_state.txt_valor)

    # Adicionando os novos campos de entrada
    txt_projeto = st.text_input("Projeto", value=st.session_state.txt_projeto)
    txt_tipo = st.text_input("Tipo", value=st.session_state.txt_tipo)
    
    txt_produto = st.text_input("Produto", value=st.session_state.txt_produto)
    txt_desc_item = st.text_input("Descrição do item", value=st.session_state.txt_desc_item)
    txt_mes_contratado = st.text_input("Mês contratado", value=st.session_state.txt_mes_contratado)
    txt_rc_contrato = st.text_input("RC, Contrato ou Direto", value=st.session_state.txt_rc_contrato)
    date_faturamento_nf = st.date_input("Data de faturamento NF", value=st.session_state.date_faturamento_nf, format="DD/MM/YYYY")
    date_recebimento_nf = st.date_input("Data Recebimento NF", value=st.session_state.date_recebimento_nf, format="DD/MM/YYYY")
    date_lancamento_nf = st.date_input("Data de lançamento NF", value=st.session_state.date_lancamento_nf, format="DD/MM/YYYY")
    txt_validacao_financeiro = st.text_input("Validação Financeiro", value=st.session_state.txt_validacao_financeiro)
    txt_mes_planilha_financeiro = st.text_input("Mês Planilha Financeiro", value=st.session_state.txt_mes_planilha_financeiro)
    txt_observacoes = st.text_area("Observações", value=st.session_state.txt_observacoes)

    
 # Botão de salvar
    if st.button("Salvar"):
        if txt_numero_nf and novo_fornecedor:
            df = load_data()

            # Verificar se NF já existe
            if txt_numero_nf in df["Número NF"].values:
                st.warning("Essa NF já foi cadastrada!")
            else:
                campos_obrigatorios_nao_preenchidos = []
                    # Verificar campos obrigatórios
                if not txt_valor:
                    campos_obrigatorios_nao_preenchidos.append("Valor")
                if not txt_produto:
                    campos_obrigatorios_nao_preenchidos.append("Produto")

                if campos_obrigatorios_nao_preenchidos:
                    st.warning(f"Os seguintes campos não foram preenchidos: {', '.join(campos_obrigatorios_nao_preenchidos)}")
       
            
                novo_registro = pd.DataFrame({
                    "Número NF": [txt_numero_nf],
                    "Data": [date_data],
                    "Valor": [txt_valor],
                    "Fornecedor": [novo_fornecedor],
                    "Descrição": [st.session_state.txt_descricao],
                    "Projeto": [txt_projeto],
                    "Tipo": [txt_tipo],
                    "Produto": [txt_produto],
                    "Descrição do item": [txt_desc_item],
                    "Mês contratado": [txt_mes_contratado],
                    "RC, Contrato ou Direto": [txt_rc_contrato],
                    "Data de faturamento NF": [date_faturamento_nf],
                    "Data Recebimento NF": [date_recebimento_nf],
                    "Data de lançamento NF": [date_lancamento_nf],
                    "Validação Financeiro": [txt_validacao_financeiro],
                    "Mês Planilha Financeiro": [txt_mes_planilha_financeiro],
                    "Observações": [txt_observacoes]
                })
                df = pd.concat([df, novo_registro], ignore_index=True)
                save_data(df)
                st.success(f"Nota Fiscal {txt_numero_nf} cadastrada com sucesso!")

                # Resetar os campos de input para os valores padrão
                st.session_state.txt_numero_nf = 0
                st.session_state.date_data = None
                st.session_state.txt_valor = 0.0
                st.session_state.novo_fornecedor = ""
                st.session_state.txt_descricao = ""
                st.session_state.txt_projeto = ""
                st.session_state.txt_tipo = ""
                st.session_state.txt_produto = ""
                st.session_state.txt_desc_item = ""
                st.session_state.txt_mes_contratado = ""
                st.session_state.txt_rc_contrato = ""
                st.session_state.date_faturamento_nf = None
                st.session_state.date_recebimento_nf = None
                st.session_state.date_lancamento_nf = None
                st.session_state.txt_validacao_financeiro = ""
                st.session_state.txt_mes_planilha_financeiro = ""
                st.session_state.txt_observacoes = ""

        else:
            st.error("Preencha os campos obrigatórios: Número NF, Fornecedor e Data da NF.")
# Se o usuário escolher "Consulta de NF"
elif menu == "Consulta de NF":
    st.header("Consulta de Notas Fiscais")
    

    # Barra lateral para filtros
    st.sidebar.header("Filtros")

    # Carregar os dados
    df = load_data()

    # Verificar se a coluna "Data" tem dados válidos
    if df["Data"].notna().any():
        data_inicio_default = df["Data"].min()
        data_fim_default = df["Data"].max()
    else:
          # Se não houver dados válidos, definimos datas padrão
        data_inicio_default = pd.to_datetime("2020-01-01").date()
        data_fim_default = pd.to_datetime("2020-01-01").date()

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

    # Definir data de início e fim com verificação de dados válidos
    data_inicio = st.sidebar.date_input(
        "Data Início", 
        data_inicio_default,  # Usa a data mínima se houver dados ou data padrão
        format="DD/MM/YYYY"
    )

    data_fim = st.sidebar.date_input(
        "Data Fim", 
        data_fim_default,  # Usa a data máxima se houver dados ou data padrão
        format="DD/MM/YYYY"
    )

    # Aplicar filtros
    df_filtrado = df[
        (df["Fornecedor"].isin(fornecedor_filtrar)) &
        (df["Data"] >= pd.to_datetime(data_inicio)) &
        (df["Data"] <= pd.to_datetime(data_fim)) &
        (df["Número NF"].isin(nota_filtrar))
    ]


      # Verifica se o DataFrame filtrado tem dados após a aplicação dos filtros
    if df_filtrado.empty:
        st.write("Nenhum registro encontrado com os filtros aplicados.")
    else:
        # Exibir os registros filtrados
        df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"]).dt.strftime("%d/%m/%Y")  # Formatar data no formato BR

        # Calcular o número total de registros
        num_linhas = len(df_filtrado)

        # Definir o número de registros por página
        registros_por_pagina = 30

        # Calcular o número total de páginas
        num_paginas = num_linhas // registros_por_pagina + (1 if num_linhas % registros_por_pagina != 0 else 0)

        # Se o usuário selecionar uma página, ou a página inicial (1)
        pagina_atual = st.session_state.get('pagina_atual', 1)  # Armazenar o estado da página em session_state

        # Calcular os índices de início e fim para o DataFrame
        inicio = (pagina_atual - 1) * registros_por_pagina
        fim = inicio + registros_por_pagina

        # Exibir a parte da tabela correspondente à página atual
        df_pagina = df_filtrado.iloc[inicio:fim]

        # Adicionar um botão expansível para selecionar as colunas
        with st.expander("Escolha as colunas para exibir"):
            # Criar uma lista de todas as colunas disponíveis
            colunas_disponiveis = df.columns.tolist()
            
            # Criar o multiselect dentro do expander
            colunas_selecionadas = st.multiselect(
                "Selecione as colunas para exibir",
                options=colunas_disponiveis,
                default=colunas_disponiveis  # Exibe todas por padrão
            )
                


    # Função para dividir a tabela em páginas
    def get_page(df, page_number, rows_per_page=len(df_filtrado)):
        start_row = (page_number - 1) * rows_per_page
        end_row = start_row + rows_per_page
        return df.iloc[start_row:end_row]

    # Variáveis de controle de página
    # Filtrar as colunas selecionadas no multiselect
    
    df_filtrado = df_filtrado[colunas_selecionadas]
    if "Valor" in colunas_selecionadas:
        df_filtrado['Valor'] = df_filtrado['Valor'].apply(lambda x: f"R$ {x:,.2f}")
    num_paginas = len(df_filtrado) // 50 + (1 if len(df_filtrado) % 50 > 0 else 0)

    # Páginas no session_state para manter o controle de navegação
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = 1

    pagina_atual = st.session_state.pagina_atual

    # Exibir a tabela da página atual (sem criar um novo DataFrame)
    df_pagina_selecionada = get_page(df_filtrado, pagina_atual)
    
    # Contar o número de linhas no DataFrame
    num_linhas = len(df_pagina_selecionada)
    # Exibir o resultado com destaque para o número
    st.markdown(f"""
        <span style='font-size: 15px; '>Notas fiscais encontradas</span>: 
        <span style='font-size: 16px; color: green; font-weight: bold;'>{num_linhas}</span>
    """, unsafe_allow_html=True)

    st.dataframe(df_pagina_selecionada)



