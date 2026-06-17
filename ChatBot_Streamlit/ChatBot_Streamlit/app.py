import os
import streamlit as st
from google.genai.errors import ServerError
from google import genai
from google.genai import types


def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():

    try:
        resposta = cliente.models.generate_content(
            model=MODELO,
            contents=converter_para_gemini(st.session_state.historico),
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCAO_SISTEMA,
                temperature=0.4,
        )
    )

        return resposta.text
    except Exception:
        return "Ocorreu um erro ao se comunicar com o Gemini, tente novamente mais tarde.   "

MODELO = "gemini-2.5-flash"
INSTRUCAO_SISTEMA = """

seja educada,gentil e honesta com o usuario.
resolva todos os problemas que esta pedindo, sempre direto ao ponto. 

"""

st.set_page_config(page_title="Chatbot Mal Educado", page_icon="🐦‍⬛")
st.title("Chatbot com Gemini")

chave_api = st.sidebar.text_input("Insira sua chave de API", type="password")

if not chave_api:
    st.warning("Você precisa inserir uma chave de API para continuar")
    st.stop()

cliente = genai.Client(api_key=chave_api)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

entrada_usuario = st.chat_input("Digite sua pergunta: ")

if entrada_usuario:
    st.session_state.historico.append(
        {
            "role":"user",
            "content":entrada_usuario
        }
    )
    with st.chat_message("user"): # Adicionando a mensagem ao chat
        st.markdown(entrada_usuario)
    
    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)

    st.session_state.historico.append(
        {
            "role":"user",
            "content":entrada_usuario
        }
    )