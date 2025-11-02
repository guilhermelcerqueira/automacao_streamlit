import streamlit as st
from datetime import datetime

# Dicionário com usuários e senhas (simples, para testes)
users = {
    "guilherme": "1234",
    "admin": "senha123"
}

def login():
    st.title("🔐 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            # Armazena o horário do login
            st.session_state.login_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            st.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# Inicializar variáveis do session_state relacionadas ao login
def init_login_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "login_time" not in st.session_state:
        st.session_state.login_time = ""

# Exibir informações de login na sidebar
def show_logged_user_sidebar():
    st.sidebar.markdown(
        f"""
        <div style="
            font-size: 13px; 
            color: #444; 
            padding: 8px 10px; 
            border-bottom: 1px solid #ddd; 
            margin-bottom: 10px;
            font-weight: 600;
        ">
            👤 Usuário logado: <strong>{st.session_state.username}</strong><br>
            🕒 Horário do login: <strong>{st.session_state.login_time}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
