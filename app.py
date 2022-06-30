import streamlit as st
import streamlit.components.v1 as stc 

st.set_page_config(
	page_title="App Predição de Sobrevida",
	page_icon="🏪",
	layout="wide",
	initial_sidebar_state="expanded",
)

def main():
	st.title("Preencha o formulário para realizar a predição")

if __name__ == '__main__':
	main()