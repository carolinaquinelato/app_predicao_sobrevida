import streamlit as st
import streamlit.components.v1 as stc
from grafico import run_grafico
from sobre import run_sobre
from lgpd import run_lgpd


def main():

    
    menu = ["Predição","Sobre","LGPD"]
    choice = st.sidebar.selectbox("Menu",menu)
       
    if choice == "Predição":
        run_grafico()
    elif choice == "Sobre":
        run_sobre()
    else:
        run_lgpd()

if __name__ == '__main__':
	main()