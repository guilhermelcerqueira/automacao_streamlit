import streamlit as st
from code.auth import login, show_logged_user_sidebar
from code.cadastro import cadastro_nf
from code.editar import editar_nf
from code.consulta import consulta_nf

# 🔒 Remove heurística de formulário financeiro do navegador (Chrome, Edge, Brave, Opera, etc)
st.markdown("""
    <meta http-equiv="Content-Security-Policy" content="form-action 'self'">
""", unsafe_allow_html=True)

# =====================================
#   LOGIN / SESSÃO
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

show_logged_user_sidebar()

# =====================================
#   TÍTULO / CSS
# =====================================

st.markdown("""
    <style>
        .titulo-customizado {
            font-size: 27px;
            font-weight: bold;
            text-align: center;
        }
    </style>
    <div class="titulo-customizado">Cadastro e Consulta de Notas Fiscais</div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .centralizado {
            display: flex;
            justify-content: center;
            text-align: center;
            font-size: 15px;
            margin-bottom: 10px;
        }
        .stRadio {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="centralizado">Escolha a opção</div>', unsafe_allow_html=True)

# =====================================
#   MENU PRINCIPAL
# =====================================

menu = st.radio(
    "",
    ("Cadastro de NF", "Editar NF", "Consulta de NF"),
    index=0,
    format_func=lambda x: f"📝 {x}" if x == "Cadastro de NF" else f"🔍 {x}" if x == "Consulta de NF" else f"✏️ {x}",
    horizontal=True
)

# =====================================
#   ROTAS DAS TELAS
# =====================================

if menu == "Cadastro de NF":
    cadastro_nf()
elif menu == "Editar NF":
    editar_nf()
elif menu == "Consulta de NF":
    consulta_nf()
