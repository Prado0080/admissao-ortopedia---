import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="Admissão Ortopedia", layout="centered")

st.title("Gerador de Admissão - Farmácia Clínica Ortopedia")

prontuario_texto = st.text_area("Cole abaixo o texto do prontuário:", height=300)

def extrair_info(texto):
    paciente = re.search(r'Paciente:\s+(.*?)\t', texto)
    ses = re.search(r'SES:\s+(\d+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)
    peso = re.search(r'Peso:\s+(\d+)', texto)  # pode estar ausente
    data_admissao = re.search(r'DATA DA ADMISSÃO:\s+(\d{2}/\d{2}/\d{4})', texto)
    diagnostico = re.search(r'DIAGNÓSTICO:\s+(.*?)\n', texto)
    mecanismo = diagnostico  # usar mesmo campo, se desejar simplificar
    data_fratura = re.search(r'DATA DA FRATURA:\s+(\d{2}/\d{2}/\d{4})', texto)
    data_cirurgia = re.search(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{4})', texto)

    return {
        "paciente": paciente.group(1) if paciente else "",
        "ses": ses.group(1) if ses else "",
        "idade": idade.group(1) if idade else "",
        "peso": peso.group(1) if peso else "—",
        "data_admissao": data_admissao.group(1) if data_admissao else datetime.today().strftime('%d/%m/%Y'),
        "data_entrevista": datetime.today().strftime('%d/%m/%Y'),
        "motivo": diagnostico.group(1) if diagnostico else "",
        "mecanismo": mecanismo.group(1) if mecanismo else "",
        "data_fratura": data_fratura.group(1) if data_fratura else "",
        "data_cirurgia": data_cirurgia.group(1) if data_cirurgia else ""
    }

if prontuario_texto:
    dados = extrair_info(prontuario_texto)

    resultado = f"""
FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {dados['paciente']}; SES: {dados['ses']}; 
Idade: {dados['idade']} anos; Peso: {dados['peso']}
Data de admissão: {dados['data_admissao']}
Data da entrevista: {dados['data_entrevista']}
----------------------------------------------------------------------------
Motivo da internação: {dados['motivo']}

Mecanismo do trauma: {dados['mecanismo']}
Data da fratura: {dados['data_fratura']}.
Data da cirurgia: {dados['data_cirurgia']}.
    """.strip()

    st.text_area("Resultado formatado:", value=resultado, height=300)
