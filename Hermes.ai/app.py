import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import requests
import base64
import pandas as pd
import matplotlib.pyplot as plt
from ms_clusterizacao.services.databricks_services import ClusterDataService
from ms_clusterizacao.services.llm_services import escolher_cluster, obter_dados_cluster_por_nome, responder_pergunta_cluster

# Estrutura Home


def home():

    abas = st.tabs(["🏠 Home", "ℹ️ Sobre nós", "💻 Soluções",
                   "🗂 Tech review"])

    # Sub-Home

    with abas[0]:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns([2, 10, 2])
        with col2:
            st.image("imagens/Home 1.png")
            st.write("")
        st.markdown("<h3 style='text-align: center;'>Transforme seus dados em insights e "
                    "revolucione a jornada do seu cliente</h3>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.divider()

        st.markdown(
            """
        <style>
        .typewriter {
        overflow: hidden;
        border-right: .15em solid orange;
        white-space: nowrap;
        letter-spacing: .15em;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        }

        @keyframes typing {
        from { width: 0 }
        to { width: 100% }
        }

        @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: white; }
        }
        </style>

        <h3 class="typewriter">Decisões baseadas em dados e tecnologia</h3>
        """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([1, 30, 1])
        with col2:
            st.image("imagens/Home 2.png")

        st.write("Nossa plataforma de inteligência de dados foi criada para ajudar empresas como a sua a personalizar a jornada do cliente de forma única.")

        col1, col2, col3 = st.columns([1, 30, 1])
        with col2:
            st.image("imagens/Home 3.png")

        st.write("Com a crescente na demanda e exigência dos clientes por uma experiência de excelência com as empresas que consomem,"
                 " é fundamental a utilização das mais novas tecnologias para poder acompanhar o mercado e seguir inovando e fidelizando os clientes.")

        st.write("A nossa solução não só vai ajudar a resolver esse problema, mas também queremos mudar a forma como sua empresa interage com os seus clientes nos diversos níveis da sua jornada.")

        col1, col2, col3 = st.columns([1, 30, 1])
        with col2:
            st.image("imagens/Home 4.png")

    # Sub-Sobre Nos

    with abas[1]:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.header("Sobre nós")
        st.divider()
        st.subheader("A Hermes AI:")
        st.write("A Hermes AI surge com uma solução inovadora para solucionar os problemas relacionados a jornada do cliente dentro das empresas, "
                 "trazendo tecnologias avançadas e uma inteligência de dados para otimizar, customizar, "
                 "recomendar e prever tendências na jornada do seu cliente desde o onboarding até o pós-venda.")
        st.write("É importante citar que existe uma tendência para os próximos anos de uma   “hiperpersonalização baseada na análise da jornada do cliente”, "
                 "como diz Ricardo Pena, CEO da PeopleXperience.")
        st.write("Pena afirma que nos próximos anos o mercado deve evoluir para níveis ainda mais segmentados e proativos,"
                 "com o uso intensivo de IA e machine learning para antecipar comportamentos e oferecer recomendações em tempo real."
                 "Com a crescente na demanda e exigência dos clientes por uma experiência de excelência com as empresas que consomem,"
                 "é fundamental a utilização das mais novas tecnologias para poder acompanhar o mercado e seguir inovando e fidelizando os clientes.")

        st.subheader("Nosso Grupo:")
        st.write("O nosso grupo se chama 'Os corujões do SQL', e somos ao todo 5 integrantes que amam e usam muito SQL no a dia a dia,"
                 " no qual temos como ponto em comum uma produtividade mais elevada em período noturnos do dia, que é o período que nos reunimos com maior frequência. "
                 "E daí veio o nome perfeito para o grupo, Os Corujões do SQL, um grupo de pessoas noturnas e facinadas pelo uso da linguagem SQL.")
        st.subheader("Os integrantes do nosso grupo:")
        st.image("imagens/integrantes do time.JPG", use_container_width=True)

    # Sub-Soluções

    with abas[2]:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.header("Soluções")
            st.divider()
        st.subheader("Análise Descritiva e Explorátoria")
        st.write(
            "Dashboard para apresentação da análise descritiva/exploratória dos dados fornecidos pela Totvs.")
        st.write("Dashboard construído na ferramenta Power BI e incorporado a nossa plataforma para facilitar a visualização das informações e análises.")
        st.write("A nossa análise tem o intuito de apresentar um resumo dos dados fornecidos e as análises realizadas em algumas variáveis.")
        st.subheader("Clusterização")
        st.write("Local destinado a apresentação e utilização por parte do usuário aos nossos modelos de clusterização, sendo o primeiro modelo disponível o K-means")
        st.subheader("Hermes AI")
        st.write("Chat AI com interface interativa para que o usuário consiga extrair insights dos resultados da clusterização e demais informações geradas pela solução.")
        st.subheader("Monitoramento")
        st.write("Feature em construção...")
        st.write(
            "Página destinada para apresentação das métricas de desempenho dos modelos")

    # Sub-Tech Review

    with abas[3]:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.header("Tech Review")
        st.divider()
        st.subheader("Documentação do Projeto")

        def mostrar_pdf(caminho_pdf):
            with open(caminho_pdf, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        mostrar_pdf("Arquivos/Escopo_Challenge_2025.pdf")

    # Sub-Contato

#    with abas[4]:
#        st.header("Contato")
#        st.write("Contato...")


# Fim da estrutura da Home


# def formulario():
#    st.title("Formulario")
#    form = st.form("my_form")
#    form.slider("Inside the form")
#    st.slider("Outside the form")

    # Now add a submit button to the form:
#    form.form_submit_button("Submit")

# Análises e Dashboard (Power BI)

def analise():
    st.header("Dashboard - Análise Descritiva e AED")

    url = "https://app.powerbi.com/view?r=eyJrIjoiYWE5MzgwYjgtZWI3Yi00MDQ5LWE3MTQtYjAyZTllNGYzNGJjIiwidCI6IjExZGJiZmUyLTg5YjgtNDU0OS1iZTEwLWNlYzM2NGU1OTU1MSIsImMiOjR9"

    components.iframe(url, width=800, height=600)

# Clusterização


def cluster():

    st.title("Clusterização")

    abas = st.tabs(["🎲 Tabela", "💡 Clusters"])

    with abas[0]:
        st.header("Tabela")

        df = pd.read_csv("Hermes.ai/Arquivos/Analise_dos_Dados_Totvs.csv")
        st.dataframe(df)

    with abas[1]:
        st.header("Clusters")

        st.image("Hermes.ai/imagens/clusterizacao_01.png",
                 use_container_width=True)

# Inteligência Artificial


def IA():
    st.title("Hermes AI")

    abas = st.tabs(["🤖 Hermes AI", "🎲 Tabela", "💡 Clusters"])

    with abas[0]:
        st.header("Chat AI")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).markdown(msg["content"])

        user_input = st.chat_input("Digite sua pergunta")

        if user_input:
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )
            st.chat_message("user").markdown(user_input)

            with st.spinner("Consultando base de conhecimento..."):
                try:

                    resultado = escolher_cluster(user_input)
                    cluster_id = resultado["cluster_id"]
                    justificativa = resultado["justificativa"]

                    # Busca dados do cluster escolhido
                    df_cluster = obter_dados_cluster(cluster_id)

                    # Resposta inicial
                    msg = (
                        f"Cluster escolhido: {cluster_id}  \n"
                        f"{len(df_cluster)} registros carregados.  \n"
                        f"Justificativa: {justificativa}"
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": msg}
                    )
                    st.chat_message("assistant").markdown(msg)

                    st.dataframe(df_cluster.head(10))

                    # Para o user fazer perguntas adicionais sobre o cluster escolhido
                    pergunta = st.text_input(
                        "Gostaria de saber algo sobre este cluster?"
                    )
                    if pergunta:
                        resposta = responder_pergunta_cluster(
                            cluster_id, pergunta)
                        st.write(resposta)

                except Exception as e:
                    st.error(f"Erro ao consultar o cluster: {e}")

    with abas[1]:
        st.header("Tabela")
        if user_input:
            with st.spinner("Carregando tabela"):
                try:
                    st.dataframe(df_cluster.head(10000))
                except Exception as e:
                    st.error(f"Erro ao consultar o cluster: {str(e)}")

    with abas[2]:
        st.header("Clusters")
        if user_input:
            with st.spinner("Carregando tabela"):
                try:
                    counts = df_cluster['CD_CLIENTE'].value_counts(
                    ).sort_index()

                    plt.figure(figsize=(8, 6))
                    plt.bar(counts.index.astype(str),
                            counts.values, color='skyblue')
                    plt.xlabel("Cluster")
                    plt.ylabel("Número de clientes")
                    plt.title("Distribuição dos clusters")
                    st.pyplot(plt)

                    # Scatter plot aleatório para visualização
                    np.random.seed(42)
                    # posições aleatórias
                    X = np.random.rand(len(df_cluster), 2)
                    labels = df_cluster['cluster'].values

                    plt.figure(figsize=(8, 6))
                    plt.scatter(X[:, 0], X[:, 1], c=labels,
                                cmap='viridis', alpha=0.7)
                    plt.xlabel("Componente X")
                    plt.ylabel("Componente Y")
                    plt.title("Distribuição dos clusters (visualização 2D)")
                    plt.colorbar(label='Cluster')
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Erro ao consultar o cluster: {str(e)}")


# Sidebar para navegação
st.sidebar.image(
    "imagens/logo_rain_of_changes.png", use_container_width=80)

with st.sidebar:
    pagina_selecionada = option_menu(
        "Menu",  # Título do menu
        ["Home",
            "Análise", "Clusterização", "Hermes AI"],  # Páginas
        icons=["house", "bar-chart", "bi-diagram-3",
               "bi-robot"],  # Ícones
        menu_icon="cast",  # Ícone do menu
        default_index=0,  # Índice da página inicial
    )

# Exibir a página selecionada
if pagina_selecionada == "Home":
    home()
elif pagina_selecionada == "Análise":
    analise()
elif pagina_selecionada == "Clusterização":
    cluster()
elif pagina_selecionada == "Hermes AI":
    IA()
