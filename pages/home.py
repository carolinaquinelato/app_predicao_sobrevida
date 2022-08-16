from tkinter import Button
import streamlit as st 
import joblib
import os
import numpy as np


st.subheader("Predição de sobrevida")
st.write("Insira as informações de um indivíduo e veja a probabilidade de sobrevivência prevista logo abaixo.")

['idade', 'raca', 'estadiamento', 'tamanho_tumor', 'estrogenio', 'progesterona']


def run_ml_app():
	st.subheader("Calculadora Online")
	loaded_model = joblib.load(open(os.path.join("models/rsf_2022.pkl"),"rb"))

    idade = st.number_input("Idade",10,100, value=54)
    estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
    tam_tumor = st.number_input("Tamanho do tumor", 20,150, value=24)
    estrog = st.radio("Estrogênio", ('Positivo','Negativo'))
    prog = st.radio("Progesterona", ('Positivo','Negativo'))

    result = {'idade':idade,
    'estadiamento' : estadiamento,
    'tam_tumor' : tam_tumor,
    'estrog' : estrog,
    'prog' : prog
    }

    encoded_result = []

    neg_pos_map = {"Negativo":0,"Positivo":1}
    estad_map = {"IIA":2,"IIB":2, "IIIA":1, "IIIB":1, "IIIC":1}

    def get_value(val,my_dict):
        for key,value in my_dict.items():
            if val == key:
                return value 

    def get_other_value(val):
        estad_map = {"IIA":2,"IIB":2, "IIIA":1, "IIIB":1, "IIIC":1}
        for key,value in estad_map.items():
            if val == key:
                return value 

    for i in result.values():
        if type(i) == int:
            encoded_result.append(i)
        elif i in ["Positivo","Negativo"]:
            res = get_value(i,neg_pos_map)
            encoded_result.append(res)
        else:
            encoded_result.append(get_other_value(i))

    