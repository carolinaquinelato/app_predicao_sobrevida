from tkinter import Button
import streamlit as st 

st.subheader("Predição de sobrevida")
st.write("Insira as informações de um indivíduo e veja a probabilidade de sobrevivência prevista logo abaixo.")
	
idade = st.number_input("Idade",10,100, value=54)
estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
tam_tumor = st.number_input("Tamanho do tumor", 20,150, value=24)
estrog = st.radio("Estrogênio", ('Positivo','Negativo'))
prog = st.radio("Progesterona", ('Positivo','Negativo'))

st.button("Predizer")