import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import requests
import base64

# Estrutura Home


def home():

    abas = st.tabs(["🏠 Home", "ℹ️ Sobre nós", "💻 Soluções",
                   "🗂 Tech review", "📬 Contato"])

    with abas[0]:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])  # o do meio ocupa mais espaço
        with col2:
            st.image("D:\Faculdade\Challenge_Totvs_2025\imagens\Home 1.png")
            st.write("")
        st.markdown("<h3 style='text-align: center;'>Transforme seus dados em insights e "
                    "revolucione a jornada do seu cliente</h3>", unsafe_allow_html=True)
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

        col1, col2, col3 = st.columns([1, 2, 1])  # o do meio ocupa mais espaço
        with col2:
            st.image("D:\Faculdade\Challenge_Totvs_2025\imagens\Home 2.png")

        st.write(
            "Nossa plataforma de inteligência de dados foi criada para ajudar empresas como a sua a personalizar a jornada do cliente de forma única.")

    with abas[1]:
        col1, col2, col3 = st.columns([1, 1, 1])  # o do meio ocupa mais espaço
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
        st.image("D:\Faculdade\Challenge_Totvs_2025\imagens\integrantes do time.JPG",use_container_width=True)


    with abas[2]:
        col1, col2, col3 = st.columns([1, 1, 1])  # o do meio ocupa mais espaço
        with col2:
            st.header("Soluções")
        st.divider()
        st.subheader("Análise Descritiva e Explorátoria")
        st.write("Projetos...")
        st.subheader("Clusterização")
        st.subheader("Monitoramento")
        st.subheader("AI")

    with abas[3]:
        col1, col2, col3 = st.columns([1, 1, 1])  # o do meio ocupa mais espaço
        with col2:
            st.header("Tech Review")
        st.divider()
        st.subheader("Documentação do Projeto")
        st.write("Docs...")
    
    with abas[4]:
        st.header("Contato")
        st.write("Contato...")


# Fim da estrutura da Home


# def formulario():
#    st.title("Formulario")
#    form = st.form("my_form")
#    form.slider("Inside the form")
#    st.slider("Outside the form")

    # Now add a submit button to the form:
#    form.form_submit_button("Submit")


def analise():
    st.header("Dashboard da Análise Descritiva e Exploratória")

    url = "https://app.powerbi.com/view?r=eyJrIjoiZGEwMzU4ZGYtYTA3OC00ZDAwLTgwOTItMzIzMDA3ZjRmOGZiIiwidCI6IjExZGJiZmUyLTg5YjgtNDU0OS1iZTEwLWNlYzM2NGU1OTU1MSIsImMiOjR9"

    components.iframe(url, width=800, height=600)


def cluster():
    st.title('Clusterização')


def monitoramento():
    st.title("Monitoramento")


# Sidebar para navegação
st.sidebar.image(
    "D:\Faculdade\Challenge_Totvs_2025\imagens\logo_rain_of_changes.png", use_container_width=80)

with st.sidebar:
    pagina_selecionada = option_menu(
        "Menu",  # Título do menu
        ["Home",
            "Análise", "Clusterização", "Monitoramento"],  # Páginas
        icons=["house", "info", "clipboard",
               "bar-chart", "gear"],  # Ícones (opcional)
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
elif pagina_selecionada == "Monitoramento":
    monitoramento()
