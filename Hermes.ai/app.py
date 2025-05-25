import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import numpy as np


# Estrutura Home
def home():
    # st.image("D:/Faculdade/Hermes.ai/imagens/mini_logo.jpg",use_container_width=100)
    st.divider()
    st.title("Nossa solução")
    st.write("A solução da Talk to Me by SophIA, vem com o objetivo de trazer funcionalidades que irão além das ferramentas convencionais de transcrição de áudio. Tudo dentro de uma plataforma web simples e intuitiva.")
# Fim da estrura da Home


def upload():
    st.title("Upload de Arquivos CSV")

    arquivos = st.file_uploader("Escolha os arquivos", type=[
                                'csv'], accept_multiple_files=True)

    if arquivos:
        st.write(f"{len(arquivos)} arquivo(s) selecionado(s).")

        if st.button("Enviar para o ms-upload"):
            files_to_send = []

            for arquivo in arquivos:
                file_tuple = (
                    "files", (arquivo.name, arquivo.getvalue(), "text/csv"))
                files_to_send.append(file_tuple)

            try:
                response = requests.post(
                    "http://localhost:8000/upload-csv/",  # ou IP público se em nuvem
                    files=files_to_send
                )

                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(
                        f"❌ Erro: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Erro de conexão com o microserviço: {e}")


def analise():
    st.title("Análise")


def cluster():
    st.title("Clusterização")


# Sidebar para navegação
st.sidebar.image(
    "D:/Faculdade/Hermes.ai/imagens/logo-backgroud.png", use_container_width=80)

with st.sidebar:
    pagina_selecionada = option_menu(
        "Menu",  # Título do menu
        ["Home", "Upload",
            "Análise", "Clusterização"],  # Páginas
        icons=["house", "info", "clipboard",
               "bar-chart", "gear"],  # Ícones (opcional)
        menu_icon="cast",  # Ícone do menu
        default_index=0,  # Índice da página inicial
    )

# Exibir a página selecionada
if pagina_selecionada == "Home":
    home()
elif pagina_selecionada == "Upload":
    upload()
elif pagina_selecionada == "Análise":
    analise()
elif pagina_selecionada == "Clusterização":
    cluster()
