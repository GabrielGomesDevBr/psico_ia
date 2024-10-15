import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import yaml
import logging

# Configuração do tema
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Função para carregar configuração
def load_config():
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        logger.info("Configuração carregada com sucesso.")
        return config
    except Exception as e:
        logger.error(f"Erro ao carregar a configuração: {e}")
        st.error("Erro ao carregar a configuração. Verifique o arquivo config.yaml.")
        return None

# Função para inicializar o modelo AI
def initialize_ai_model(api_key):
    try:
        os.environ['GOOGLE_API_KEY'] = api_key
        model = ChatGoogleGenerativeAI(model='gemini-pro')
        logger.info("Modelo AI inicializado com sucesso.")
        return model
    except Exception as e:
        logger.error(f"Erro ao inicializar o modelo AI: {e}")
        st.error("Erro ao inicializar o modelo AI. Verifique sua chave API.")
        return None

# Template do prompt
template = '''
Você é um assistente chamado PsicoIA, especializado em auxiliar psicólogos na geração de relatórios psicológicos. Suas atribuições incluem:
- Atuar como um especialista em psicologia, oferecendo insights baseados em evidências científicas.
- Gerar relatórios psicológicos detalhados e profissionais.
- Fornecer sugestões de intervenções terapêuticas adequadas.
- Oferecer recomendações para acompanhamento e tratamento.

Você deve responder apenas a questões relacionadas à psicologia e geração de relatórios psicológicos.

Dados do paciente:
Nome: {nome}
Idade: {idade} anos
Gênero: {genero}
Motivo da consulta: {motivo_consulta}
Diagnóstico prévio: {diagnostico_previo}
Detalhes do diagnóstico (se aplicável): {diagnostico_detalhes}
Histórico médico relevante: {historico_medico}
Sintomas principais: {sintomas_principais}
Duração dos sintomas: {duracao_sintomas}
Fatores estressores atuais: {fatores_estressores}
Histórico familiar de saúde mental: {historico_familiar}
Medicações atuais: {medicacoes}
Abordagem terapêutica preferida: {abordagem_terapeutica}

Com base nessas informações, forneça um relatório psicológico completo e profissional, incluindo:
1. Resumo da apresentação do paciente e motivo da consulta.
2. Avaliação dos sintomas e seu impacto na vida do paciente.
3. Análise do impacto dos fatores estressores na saúde mental do paciente.
4. Considerações sobre o histórico médico e familiar.
5. Recomendações de intervenções terapêuticas baseadas na abordagem preferida.
6. Sugestões para acompanhamento e possíveis encaminhamentos.
7. Objetivos terapêuticos iniciais e plano de tratamento proposto.

{instrucoes_diagnostico}

Forneça respostas detalhadas e profissionais, simulando o relatório que um psicólogo experiente produziria. Evite generalizações e foque nas informações específicas do paciente.

Formate o relatório utilizando Markdown para melhor legibilidade.
'''

prompt_template = PromptTemplate(template=template, input_variables=[
    "nome", "idade", "genero", "motivo_consulta", "diagnostico_previo", "diagnostico_detalhes",
    "historico_medico", "sintomas_principais", "duracao_sintomas", "fatores_estressores", 
    "historico_familiar", "medicacoes", "abordagem_terapeutica", "instrucoes_diagnostico"
])

# Listas de opções
generos = ['Masculino', 'Feminino', 'Não-binário', 'Prefiro não especificar']
abordagens_terapeuticas = ['Terapia Cognitivo-Comportamental', 'Psicanálise', 'Terapia Humanista', 'Terapia Sistêmica', 'Terapia Integrativa', 'Terapia ABA']

# Configuração da página Streamlit
st.set_page_config(page_title="Psico-IA - Assistente de Relatórios Psicológicos", layout="wide",  page_icon="🧠",)

# Aplicar estilo personalizado
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #f1f1f1, #e1e1e1);
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
        padding: 1rem;
    }
    .sidebar .sidebar-content a {
        color: #3498db;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title('Psico-IA - Assistente de Relatórios Psicológicos')
st.markdown('---')

# Carregar configuração
config = load_config()
if config is None:
    st.stop()

# Inicializar modelo AI
ai_model = initialize_ai_model(config['GOOGLE_API_KEY'])
if ai_model is None:
    st.stop()

# Interface do usuário
col1, col2 = st.columns(2)

with col1:
    st.subheader('Informações do Paciente')
    nome = st.text_input('Nome do paciente:')
    idade = st.number_input('Idade:', min_value=0, max_value=120, step=1)
    genero = st.selectbox("Gênero:", generos)
    motivo_consulta = st.text_area('Motivo da consulta:')
    diagnostico_previo = st.selectbox('Paciente possui diagnóstico prévio?', ['Não', 'Sim'])
    diagnostico_detalhes = st.text_input('Caso tenha sinalizado que sim acima, insira aqui o diagnóstico:')
    historico_medico = st.text_area('Histórico médico relevante:')

with col2:
    st.subheader('Detalhes Clínicos')
    sintomas_principais = st.text_area('Sintomas principais:')
    duracao_sintomas = st.text_input('Duração dos sintomas:')
    fatores_estressores = st.text_area('Fatores estressores atuais:')
    historico_familiar = st.text_area('Histórico familiar de saúde mental:')
    medicacoes = st.text_area('Medicações atuais:')
    abordagem_terapeutica = st.selectbox('Abordagem terapêutica preferida:', abordagens_terapeuticas)

st.markdown('---')

if st.button('Gerar Relatório Psicológico'):
    logger.info("Botão 'Gerar Relatório Psicológico' pressionado.")
    if not all([nome, idade, motivo_consulta, sintomas_principais]):
        st.warning('Por favor, preencha todos os campos obrigatórios.')
    else:
        try:
            with st.spinner('Gerando relatório... Por favor, aguarde.'):
                # Definir instruções baseadas no diagnóstico prévio
                if diagnostico_previo == 'Sim':
                    instrucoes_diagnostico = "Como o paciente possui um diagnóstico prévio, inclua considerações sobre este diagnóstico no relatório e como ele se relaciona com os sintomas e o tratamento proposto."
                else:
                    instrucoes_diagnostico = "Como o paciente não possui um diagnóstico prévio, evite especulações sobre possíveis diagnósticos. Foque na descrição dos sintomas e no plano de tratamento sem fazer prognósticos específicos."

                prompt = prompt_template.format(
                    nome=nome,
                    idade=idade,
                    genero=genero,
                    motivo_consulta=motivo_consulta,
                    diagnostico_previo=diagnostico_previo,
                    diagnostico_detalhes=diagnostico_detalhes,
                    historico_medico=historico_medico,
                    sintomas_principais=sintomas_principais,
                    duracao_sintomas=duracao_sintomas,
                    fatores_estressores=fatores_estressores,
                    historico_familiar=historico_familiar,
                    medicacoes=medicacoes,
                    abordagem_terapeutica=abordagem_terapeutica,
                    instrucoes_diagnostico=instrucoes_diagnostico
                )
                logger.info("Prompt gerado com sucesso.")

                logger.info("Invocando modelo AI...")
                response = ai_model.invoke(prompt)
                logger.info("Resposta do modelo AI recebida.")

            st.success('Relatório gerado com sucesso!')
            st.subheader('Relatório Psicológico Gerado:')
            st.markdown(response.content)
            logger.info("Relatório exibido com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            st.error(f"Ocorreu um erro ao gerar o relatório: {e}")

# Sidebar
st.sidebar.title("Sobre a Psico-IA")
st.sidebar.info("""
A Psico-IA é uma ferramenta avançada de inteligência artificial desenvolvida pela AperData para otimizar e elevar a qualidade da geração de relatórios psicológicos, oferecendo suporte especializado e eficiente aos profissionais de psicologia.
""")

st.sidebar.title("Entre em Contato")
st.sidebar.markdown("""
Para soluções de IA sob medida ou suporte:

- 🌐 [aperdata.com](https://aperdata.com)
- 📱 WhatsApp: **11 98854-3437**
- 📧 Email: **gabriel@aperdata.com**
""")

logger.info("Aplicação Streamlit iniciada e pronta para uso.")
