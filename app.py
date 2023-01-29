import streamlit as st


import joblib
import streamlit.components.v1 as stc 
import joblib
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

from grafico import run_grafico
# from streamlit_option_menu import option_menu


def main():
	# menu = ["Sobre", "Predição"]
	# choice = st.sidebar.selectbox("Menu",menu)

	# if choice == "Sobre":
	# 	st.markdown("<h1 style='text-align: center; color:#666a68;'>Predição de Sobrevida para Câncer de Mama</h1>", unsafe_allow_html=True)
	# 	st.write('***Nota: esse modelo é um projeto de pesquisa e sua acurácia não pode ser garantida!***')
	# elif choice == "Predição":
	run_grafico()

			
if __name__ == "__main__":
    main()
