
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as stc 
from grafico import run_grafico

st.set_page_config(
	page_title="App Predição de Sobrevida",
	page_icon="🎗️",
	layout="wide"
)


def main():
	with st.sidebar:
		selected = option_menu(
			menu_title = 'Menu',
			options = ["Sobre", "Predição"],
	)

	if selected == "Sobre":
		st.markdown("<h1 style='text-align: center; color:#666a68;'>Predição de Sobrevida para Câncer de Mama</h1>", unsafe_allow_html=True)
		st.write('***Nota: esse modelo é um projeto de pesquisa e sua acurácia não pode ser garantida!***')
	if selected == "Predição":
		run_grafico()

if __name__ == '__main__':
	main