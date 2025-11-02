# 📄 Sistema de Gestão de Notas Fiscais (Streamlit)

Aplicação desenvolvida em **Python + Streamlit** para gestão de Notas Fiscais, substituindo planilhas manuais por um sistema web simples, padronizado e seguro.

O objetivo principal é evitar erros comuns em controles feitos no Excel, como:
- datas preenchidas incorretamente
- fornecedores com nomes divergentes
- digitação livre sem validação
- informações duplicadas ou incompletas
- dificuldade de consulta e filtragem de registros

Este sistema serve como **projeto de portfólio**, demonstrando boas práticas de desenvolvimento, modularização, autenticação, validação de dados e integração com arquivos externos.

🔗 **Versão online do app:**  
https://automacaonfs.streamlit.app/

<p align="center">
  <img src="https://github.com/user-attachments/assets/13e16463-635d-4536-acac-3aa3cda0baf2" width="720">
</p>

---

## ✨ Funcionalidades

| Função | Descrição |
|--------|-----------|
| ✅ Cadastro de NF | Formulário com validação de campos e preenchimento assistido |
| ✅ Edição de NF | Permite atualizar qualquer campo de uma NF existente |
| ✅ Exclusão de NF | Remove o registro diretamente do banco Excel |
| ✅ Consulta avançada | Filtros por data, fornecedor, número de NF e vários campos |
| ✅ Paginação | Visualização de grandes volumes sem travar a interface |
| ✅ Autenticação | Login simples com controle de sessão (`st.session_state`) |
| ✅ Dicionário de validação | Campos "Projeto", "Tipo" e "Produto" só aceitam valores cadastrados |
| ✅ Armazenamento local | Os dados ficam em um arquivo Excel (`/data/registro.xlsx`) |
| ✅ Código modular | Cada tela é um módulo separado dentro da pasta `code/` |

---

## 🔐 Login de Demonstração

Usuário: admin
Senha: senha123


O login é validado via sessão (`streamlit.session_state`) e exibe o usuário logado e o horário de acesso na sidebar.

---

```md
## 🗂️ Estrutura do Projeto

📁 automacao_streamlit/
├── app.py
├── requirements.txt
├── README.md
│
├── 📁 code/
│   ├── auth.py          → Tela de login e sessão
│   ├── cadastro.py      → Cadastro de NF
│   ├── consulta.py      → Tela de filtros e consulta
│   ├── editar.py        → Edição e exclusão de NF
│   ├── database.py      → Leitura e escrita no Excel
│
└── 📁 data/
    ├── registro.xlsx     → Base principal (Cadastro de NF)
    ├── dicionario.xlsx   → Dicionário de validação (Projeto, Tipo, Produto)
```

---

## 📊 Padronização de Dados com "Dicionário"

Para evitar poluição no banco (ex: `Fornecedor X`, `Fornecedor-X`, `FORNECEDOR X`), o sistema usa um arquivo separado (`data/dicionario.xlsx`) contendo:

- Projeto  
- Tipo  
- Produto  
- Descrição  

O cadastro permite selecionar apenas valores já existentes no dicionário, evitando divergências e erros de digitação. Ao cadastrar uma nova nota, o sistema exibirá os fornecedores já cadastrados. Caso seja necessário incluir um novo fornecedor, também haverá a opção de adicioná-lo.

---


## 🔮 Futuras Evoluções (Roadmap)

| Status | Funcionalidade |
|--------|----------------|
| ✅ | Migrar backend de Excel para Google Sheets (multiusuário online) |
| ✅ | Versão com banco SQLite + autenticação real e níveis de permissão |
| ✅ | Página **Dashboard** com análises gráficas (total por período, ranking de fornecedores, curva de despesas etc.) |
| ✅ | Exportação de relatórios (PDF, CSV) direto pelo app |
| ✅ | Upload de anexos da NF (PDF, XML) |
| ✅ | Logs de auditoria: *"quem editou o quê?"* |
| ⏳ | Alternativa de backend: Google Sheets como banco de dados |
| ⏳ | Integração com Power BI / Looker Studio |
| ⏳ | Envio automático de e-mail após nova NF cadastrada |
| ⏳ | Notificações por Telegram / Teams / Slack |
| ⏳ | Detector de duplicidade de NF com IA |
| 🔄 | Migração de controle de versão por arquivo → histórico de edição automatizado |
| 🧪 | Possibilidade de API REST para integrar ERPs |
| 💡 | Página extra de análises financeiras dentro do app (em planejamento) |

---

### 📌 Sobre a migração para Google Sheets

O sistema pode ser adaptado para trocar:

```
Leitura atual:     pandas.read_excel()
Gravação atual:    pandas.to_excel()

Alternativa futura:
✅ Leitura: gspread / Google Sheets API → sheet.get_all_records()
✅ Gravação: sheet.update() ou atualização por range dinâmico
```

Isso permite:

- ✅ Edição simultânea por múltiplos usuários
- ✅ Controle de histórico e versionamento nativo do Google
- ✅ Evitar upload/download manual de arquivos
- ✅ Uso real em equipe — não apenas local

---

### 🧠 Recursos Planejados para Dashboard

✅ Total gasto por período  
✅ Top 10 fornecedores por volume  
✅ Evolução temporal de gastos (linha / área)  
✅ Indicador de contratos vencendo  
✅ Pie chart: despesas por categoria / projeto  

*(será adicionado em página separada do menu — “Dashboard”)*

---

### 🛠️ Tecnologias Utilizadas

| Categoria | Ferramenta |
|-----------|------------|
| Backend | Python |
| Interface Web | Streamlit |
| Manipulação de Dados | Pandas |
| Arquivo Local | Excel (.xlsx) via OpenPyXL |
| Versionamento | Git + GitHub |
| Deploy | Streamlit Cloud |
| Futuro Backend | Google Sheets API / SQLite |

---

### 👤 Autor

Desenvolvido por **Guilherme Cerqueira**  
📌 Projeto de portfólio — automação de processos financeiros e de compras  
🔗 App online: https://automacaonfs.streamlit.app/


