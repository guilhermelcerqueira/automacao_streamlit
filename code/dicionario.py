import pandas as pd

def carregar_dicionario():
    """
    Lê o arquivo Excel contendo as colunas: Projeto, Tipo, Produto e Descrição.
    Retorna três dicionários organizados para uso nos selectboxes:
        - projetos: lista única de projetos
        - tipos_por_projeto: {projeto: [tipos]}
        - produtos_por_tipo: {tipo: [produtos]}
    """
    df = pd.read_excel("data/dicionario_3.xlsx")

    # Garantir que as colunas necessárias existam
    required_cols = ["Projeto", "Tipo", "Produto", "Descrição"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' ausente no arquivo Excel.")

    # Remover linhas vazias
    df = df.dropna(subset=["Projeto", "Tipo", "Produto"])

    # Criar listas e dicionários para os selectboxes
    projetos = sorted(df["Projeto"].unique().tolist())

    tipos_por_projeto = {
        projeto: sorted(df[df["Projeto"] == projeto]["Tipo"].unique().tolist())
        for projeto in projetos
    }

    produtos_por_tipo = {
        tipo: sorted(df[df["Tipo"] == tipo]["Produto"].unique().tolist())
        for tipo in df["Tipo"].unique()
    }

    return {
        "projetos": projetos,
        "tipos_por_projeto": tipos_por_projeto,
        "produtos_por_tipo": produtos_por_tipo,
        "descricao": df  # opcional: mantém o dataframe completo se quiser usar a coluna Descrição
    }
