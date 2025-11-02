import streamlit as st
import pandas as pd
from code.database import load_data, save_data
from code.dicionario import carregar_dicionario

# ===============================
# TELA DE CADASTRO DE NF
# ===============================

def cadastro_nf():

    st.header("Cadastro de Notas Fiscais")
    
    import locale
   
    df = load_data()

    # Função para inicializar os campos no session_state com valores padrão
    def init_session_state(key, default_value):
        """Função genérica para inicializar valores no session_state."""
        if key not in st.session_state:
            st.session_state[key] = default_value

    # Inicializando os valores necessários
    init_session_state("txt_numero_nf", 0.0)
    init_session_state("date_data", None)
    init_session_state("txt_valor", 0.0)
    init_session_state("txt_fornecedor", "")
    init_session_state("txt_descricao", "")
    init_session_state("txt_projeto", "")
    init_session_state("txt_tipo", "")
    init_session_state("txt_ciclo", "N/A")
    init_session_state("txt_produto", "")
    init_session_state("txt_desc_item", "")
    init_session_state("txt_mes_contratado", "")
    init_session_state("txt_rc_contrato", "")
    init_session_state("date_faturamento_nf", None)
    init_session_state("date_recebimento_nf", None)
    init_session_state("date_lancamento_nf", None)
    init_session_state("txt_validacao_financeiro", "")
    init_session_state("txt_mes_planilha_financeiro", "")
    init_session_state("txt_observacoes", "")

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

    # Carregar o novo dicionário
    dicionario = carregar_dicionario()

    # --- Projeto ---
    txt_projeto = st.selectbox("Projeto", options=[""] + dicionario["projetos"], key="select_projeto")

    # --- Tipo ---
    tipos_disponiveis = []
    if txt_projeto:
        tipos_disponiveis = dicionario["tipos_por_projeto"].get(txt_projeto, [])
    txt_tipo = st.selectbox("Tipo", options=[""] + tipos_disponiveis, key="select_tipo")

    # --- Produto ---
    produtos_disponiveis = []
    if txt_tipo:
        produtos_disponiveis = dicionario["produtos_por_tipo"].get(txt_tipo, [])
    txt_produto = st.selectbox("Produto", options=[""] + produtos_disponiveis, key="select_produto")

    # --- Descrição automática (opcional) ---
    descricao_produto = ""
    if txt_produto:
        df_desc = dicionario["descricao"]
        linha = df_desc[df_desc["Produto"] == txt_produto]
        if not linha.empty:
            descricao_produto = linha.iloc[0]["Descrição"]

    st.text_input("Descrição do item", value=descricao_produto, disabled=True, key="descricao_produto_fixa")

    txt_desc_item = st.text_input("Descrição do item", value=st.session_state.txt_desc_item)

    meses_planilha = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    txt_mes_contratado = st.selectbox("Mês contratado", options=[""]+ meses_planilha, key="mes_contratado")

    rc_opcoes = ["Mensal", "Semestral", "Anual"]
    txt_rc_contrato = st.selectbox("Modelo de contratação", options=[""]+ rc_opcoes)

    date_faturamento_nf = st.date_input("Data de faturamento NF", value=st.session_state.date_faturamento_nf, format="DD/MM/YYYY")
    date_recebimento_nf = st.date_input("Data Recebimento NF", value=st.session_state.date_recebimento_nf, format="DD/MM/YYYY")
    date_lancamento_nf = st.date_input("Data de lançamento NF", value=st.session_state.date_lancamento_nf, format="DD/MM/YYYY")

    validacoes_financeiro = ["Aprovado", "Aguardando aprovação", "Reprovado"]
    txt_validacao_financeiro = st.selectbox("Validação Financeiro", options=[""]+ validacoes_financeiro)
    txt_mes_planilha_financeiro = st.selectbox("Mês Planilha Financeiro", options=[""]+ meses_planilha)
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
                    "Modelo de Contrato": [txt_rc_contrato],
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
