import streamlit as st
import numpy as nu
import plotly.express as px
from  RotasFrequentes.RotasFrequentesCtx import *

rotas = get_rotas_frequentes().rotasFrequentesFrame
st.title("GoRoute")
st.sidebar.title("GoRoute")

st.markdown("Varificação de Rotas Frequentes e Áreas mais lucrativas")
st.sidebar.markdown("Varificação de Rotas Frequentes e Áreas mais lucrativas")

st.sidebar.header("Escolha uma das opções:")
choice = st.sidebar.radio('',('Rotas Frequentes', 'Áreas Lucrativas'))

if choice == 'Rotas Frequentes':
    st.write("Rotas Frequentes")
    st.write(rotas)
else:
    st.write("Áreas Lucrativas")