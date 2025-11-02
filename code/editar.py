import streamlit as st
import pandas as pd
from code.database import load_data, save_data

# ===============================
# TELA DE EDIÇÃO / EXCLUSÃO DE NF
# ===============================

def editar_nf():

    # Carregar os dados
    df = load_data()

    # Selectbox para escolher entre "Editar" ou "Excluir"
    action = st.selectbox("Escolha a ação", ["Editar", "Excluir"])

    # ============================
    # MODO EDITAR
    # ============================
    if action == "Editar":
        st.header("Editar Notas Fiscais")

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
            txt_descricao = st.text_area("Descrição", value[nf_data["Descrição"]])

            # Adicionando os novos campos de entrada com os dados atuais da NF
            txt_projeto = st.text_input("Projeto", value=nf_data["Projeto"])
            txt_tipo = st.text_input("Tipo", value=nf_data["Tipo"])
            txt_produto = st.text_input("Produto", value[nf_data["Produto"]])
            txt_desc_item = st.text_input("Descrição do item", value[nf_data["Descrição do item"]])
            txt_mes_contratado = st.text_input("Mês contratado", value=nf_data["Mês contratado"])
            txt_rc_contrato = st.text_input("Modelo de Contrato", value[nf_data["Modelo de Contrato"]])
            date_faturamento_nf = st.date_input("Data de faturamento NF", value=pd.to_datetime(nf_data["Data de faturamento NF"]))
            date_recebimento_nf = st.date_input("Data Recebimento NF", value=pd.to_datetime(nf_data["Data Recebimento NF"]))
            date_lancamento_nf = st.date_input("Data de lançamento NF", value=pd.to_datetime(nf_data["Data de lançamento NF"]))
            txt_validacao_financeiro = st.text_input("Validação Financeiro", value[nf_data["Validação Financeiro"]])
            txt_mes_planilha_financeiro = st.text_input("Mês Planilha Financeiro", value[nf_data["Mês Planilha Financeiro"]])
            txt_observacoes = st.text_area("Observações", value[nf_data["Observações"]])

            # Botão de salvar
            if st.button("Salvar Alterações"):
                # Atualiza os dados da NF selecionada
                df.loc[df["Número NF"] == nf_selecionada, [
                    "Data", "Valor", "Fornecedor", "Descrição", "Projeto", "Tipo", "Produto", 
                    "Descrição do item", "Mês contratado", "Modelo de Contrato", 
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
                nf_selecionada = "Selecione..."  # Resetando o selectbox manualmente

    # ============================
    # MODO EXCLUIR
    # ============================
    elif action == "Excluir":
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
