import streamlit as st
import pandas as pd
from code.database import load_data

# ===============================
# TELA DE CONSULTA DE NF
# ===============================

def consulta_nf():
    
    
    st.header("Consulta de Notas Fiscais")
    st.write("")   # Linha neutra que quebra a heurística do navegador
    
    # Carregar os dados PRIMEIRO (evita renderização da sidebar antes dos tipos corretos)
    df = load_data()
    
    # Garantir que "Número NF" seja string para evitar heurísticas do navegador
    if "Número NF" in df.columns:
        df["Número NF"] = df["Número NF"].astype(str)

    # Barra lateral para filtros (renderiza após garantir tipos)
    st.sidebar.header("Filtros")

    # Verificar se a coluna "Data" tem dados válidos
    if "Data" in df.columns and df["Data"].notna().any():
        data_inicio_default = df["Data"].min()
        data_fim_default = df["Data"].max()
    else:
        # Se não houver dados válidos, definimos datas padrão
        data_inicio_default = pd.to_datetime("2020-01-01").date()
        data_fim_default = pd.to_datetime("2020-01-01").date()

    # Filtros
    nota_filtrar = st.sidebar.multiselect(
        "Número NF",
        options=list(df["Número NF"].unique()) if "Número NF" in df.columns else [],
        default=[]  # Filtro vazio por padrão
    )

    fornecedor_filtrar = st.sidebar.multiselect(
        "Fornecedor",
        options=list(df["Fornecedor"].unique()) if "Fornecedor" in df.columns else [],
        default=[]
    )

    # Se nenhum fornecedor for selecionado, incluir todos os fornecedores
    if not fornecedor_filtrar and "Fornecedor" in df.columns:
        fornecedor_filtrar = df["Fornecedor"].unique()

    # Se nenhum número de NF for selecionado, incluir todos os números de NF
    if not nota_filtrar and "Número NF" in df.columns:
        nota_filtrar = df["Número NF"].unique()

    # Definir data de início e fim com verificação de dados válidos
    data_inicio = st.sidebar.date_input(
        "Data Início", 
        data_inicio_default
    )

    data_fim = st.sidebar.date_input(
        "Data Fim", 
        data_fim_default
    )

    # Aplicar filtros (garantir colunas existirem)
    condicoes = True
    if "Fornecedor" in df.columns:
        condicoes = condicoes & (df["Fornecedor"].isin(fornecedor_filtrar))
    if "Data" in df.columns:
        condicoes = condicoes & (df["Data"] >= pd.to_datetime(data_inicio)) & (df["Data"] <= pd.to_datetime(data_fim))
    if "Número NF" in df.columns:
        condicoes = condicoes & (df["Número NF"].isin(nota_filtrar))

    df_filtrado = df[condicoes] if not isinstance(condicoes, bool) else df.copy()

    # Verifica se o DataFrame filtrado tem dados após a aplicação dos filtros
    if df_filtrado.empty:
        st.write("Nenhum registro encontrado com os filtros aplicados.")
    else:
        # Exibir os registros filtrados (formatação de datas se existirem)
        if "Data" in df_filtrado.columns:
            df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"]).dt.strftime("%d/%m/%Y")
        if "Data de faturamento NF" in df_filtrado.columns:
            df_filtrado["Data de faturamento NF"] = pd.to_datetime(df_filtrado["Data de faturamento NF"]).dt.strftime("%d/%m/%Y")
        if "Data de lançamento NF" in df_filtrado.columns:
            df_filtrado["Data de lançamento NF"] = pd.to_datetime(df_filtrado["Data de lançamento NF"]).dt.strftime("%d/%m/%Y")
        if "Data Recebimento NF" in df_filtrado.columns:
            df_filtrado["Data Recebimento NF"] = pd.to_datetime(df_filtrado["Data Recebimento NF"]).dt.strftime("%d/%m/%Y")

        # Definir o número de registros por página
        registros_por_pagina = 30

        # Calcular o número total de páginas
        num_linhas_total = len(df_filtrado)
        num_paginas = num_linhas_total // registros_por_pagina + (1 if num_linhas_total % registros_por_pagina != 0 else 0)

        # Páginas no session_state para manter o controle de navegação
        if "pagina_atual" not in st.session_state:
            st.session_state.pagina_atual = 1

        pagina_atual = st.session_state.pagina_atual

        # Calcular os índices de início e fim para o DataFrame
        inicio = (pagina_atual - 1) * registros_por_pagina
        fim = inicio + registros_por_pagina

        # Adicionar um botão expansível para selecionar as colunas
        with st.expander("Escolha as colunas para exibir"):
            # Criar uma lista de todas as colunas disponíveis (baseado no df original)
            colunas_disponiveis = df.columns.tolist()
            
            # Criar o multiselect dentro do expander
            colunas_selecionadas = st.multiselect(
                "Selecione as colunas para exibir",
                options=colunas_disponiveis,
                default=colunas_disponiveis  # Exibe todas por padrão
            )

        # Se nenhuma coluna foi selecionada (por segurança), exibir todas
        if not colunas_selecionadas:
            colunas_selecionadas = df.columns.tolist()

        # Filtrar as colunas selecionadas no DataFrame filtrado
        df_filtrado = df_filtrado.loc[:, [c for c in colunas_selecionadas if c in df_filtrado.columns]]

        # Formatar campo Valor se existir e estiver selecionado
        if "Valor" in df_filtrado.columns and "Valor" in colunas_selecionadas:
            # Tentar converter para numérico antes de formatar
            df_filtrado["Valor"] = pd.to_numeric(df_filtrado["Valor"], errors="coerce").fillna(0.0)
            df_filtrado["Valor"] = df_filtrado["Valor"].apply(lambda x: f"R$ {x:,.2f}")

        # Função para dividir a tabela em páginas
        def get_page(df_local, page_number, rows_per_page=registros_por_pagina):
            start_row = (page_number - 1) * rows_per_page
            end_row = start_row + rows_per_page
            return df_local.iloc[start_row:end_row]

        # Extrair a página atual
        df_pagina_selecionada = get_page(df_filtrado, pagina_atual, registros_por_pagina)

        # Contar o número de linhas exibidas na página
        num_linhas = len(df_pagina_selecionada)

        # Exibir contagem e tabela
        st.markdown(f"""
            <span style='font-size: 15px; '>Notas fiscais encontradas</span>: 
            <span style='font-size: 16px; color: green; font-weight: bold;'>{num_linhas}</span>
        """, unsafe_allow_html=True)

        st.dataframe(df_pagina_selecionada)
        st.write(f"Mostrando {len(df_pagina_selecionada)} registros de {len(df_filtrado)} filtrados.")
