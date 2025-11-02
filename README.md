----- INÍCIO README -----
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

## 🗂️ Estrutura do Projeto
automacao_streamlit/
│ app.py
│ requirements.txt
│ README.md
│
├── code/
│ ├── auth.py → Tela de login e sessão
│ ├── cadastro.py → Cadastro de NF
│ ├── consulta.py → Tela de filtros e consulta
│ ├── editar.py → Edição e exclusão de NF
│ ├── database.py → Leitura e escrita no Excel
│
└── data/
├── registro.xlsx → Base principal (CADASTRO DE NF)
├── dicionario.xlsx → Dicionário de validação (Projeto, Tipo, Produto



---

## 📊 Padronização de Dados com "Dicionário"

Para evitar poluição no banco (ex: `Fornecedor X`, `Fornecedor-X`, `FORNECEDOR X`), o sistema usa um arquivo separado (`data/dicionario.xlsx`) contendo:

- Projeto  
- Tipo  
- Produto  
- Descrição  

O cadastro só permite selecionar valores existentes no dicionário, evitando divergências e erros de digitação.

---

## 🖼️ Capturas de Tela

> *(Imagens devem ser adicionadas manualmente pelo autor)*  
> Exemplo de formato:  
🔐 Tela de Login

<img width="809" height="512" alt="image" src="https://github.com/user-attachments/assets/c86faa7f-2486-41b7-b9ef-8b17e25cc3b4" />

📝 Cadastro de Nota Fiscal

<img width="1704" height="932" alt="image" src="https://github.com/user-attachments/assets/60fa7059-4e5d-4ec6-9641-09544958a742" />

✏️ Edição de Nota Fiscal

<img width="1816" height="813" alt="image" src="https://github.com/user-attachments/assets/c725d4c2-8638-4042-b602-2f1260f67569" />

🔍 Consulta com filtros

<img width="1770" height="749" alt="image" src="https://github.com/user-attachments/assets/52e440c7-209d-475a-9dbe-54b51f823997" />

🔄 Futuras Evoluções (Roadmap)

✅ Migrar o backend de Excel para Google Sheets (multiusuário online)
✅ Versão com banco SQLite + autenticação real e níveis de permissão
✅ Página "Dashboard" com análises gráficas:

total por período

ranking de fornecedores

curva de despesas ao longo do tempo
✅ Exportação de relatórios (PDF, CSV) direto pelo app
✅ Upload de anexos da NF (PDF, XML)
✅ Logs de auditoria: "quem editou o quê?"

☁️ Possibilidade futura: Google Sheets como banco de dados

O sistema pode ser adaptado para trocar:

pandas.read_excel()  →  Google Sheets API (gspread)
pandas.to_excel()    →  update_sheet()

Isso permite:

acesso simultâneo por múltiplos usuários

planilha com histórico de versões

edição sem depender de download/upload de arquivos

📚 Tecnologias Utilizadas
Tecnologia	Uso
✅ Python	Backend
✅ Streamlit	Interface Web
✅ Pandas	Manipulação de dados
✅ OpenPyXL	Leitura e gravação de Excel
✅ Git + GitHub	Versionamento
✅ (Futuro) Google Sheets API	Alternativa ao Excel
✅ (Futuro) SQLite	Banco de dados local

👔 Autor

Desenvolvido por Guilherme Lima
📌 Projeto de portfólio — automação de processos de compras / financeiro
