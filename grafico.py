
import joblib
from matplotlib.ft2font import FIXED_WIDTH
import streamlit as st
import streamlit.components.v1 as stc 
import joblib
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

st.set_page_config(
	page_title="App Predição de Sobrevida",
	page_icon="🎗️",
	initial_sidebar_state='auto'
)

# Load ML Models

def load_model(model_file):
	model = joblib.load(open(os.path.join(model_file),"rb"))
	return model


def run_grafico():
	st.markdown("<h1 style='text-align: center; color:#666a68;'>Predição de Sobrevida para Câncer de Mama</h1>", unsafe_allow_html=True)
	
	with st.sidebar:
		model = load_model('model/rsf_2022.pkl')

		# st.markdown("<h2 style='text-align: center; color: #989e9a;'>Selecione as informações abaixo para realizar a predição de sobrevida</h2>", unsafe_allow_html=True)

		idade = st.number_input("Idade",1,100, value=54)
		prog = st.radio("Progesterona", ('Positivo','Negativo'))
		tam_tumor = st.slider("Tamanho do tumor: ", min_value=1, max_value=150, value=24)
		estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
		estrog = st.radio("Estrogênio", ('Positivo','Negativo'))
		faixa = st.slider("Anos de visualização:", min_value=3, max_value=10, value=5)
		# submitted = st.form_submit_button(label="Submeter")
		submitted = st.button(label="Submeter")
		st.write('')
		st.write('')
	
		if idade>53:
			idade =1
		else:
			idade=2

		if tam_tumor>24:
			tam_tumor=1
		else:
			tam_tumor=2

		result = {'idade':idade,
		'estadiamento' : estadiamento,
		'tam_tumor' : tam_tumor,
		'estrog' : estrog,
		'prog' : prog
		}

		encoded_result = []

		
		neg_pos_map = {"Negativo":0,"Positivo":1}

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


	if submitted:
		single_sample = np.array(encoded_result).reshape(1,-1)

		col1, col2 = st.columns(2)
		with col1:
		#gráfico 1
			surv = model.predict_survival_function(single_sample, return_array=True)
			
			survival = pd.DataFrame({'Probabilidade de Sobrevida': value for value in surv})
			survival['Meses'] = survival.index+1
                        max_meses = faixa*12
			survival = survival.head(max_meses)
			

			p1 = px.line(survival,x='Meses',y='Probabilidade de Sobrevida', markers=False, title="Curva de probabilidade de sobrevida")
			p1.update_layout(autosize=True)
			p1.update_traces(line_color='#666a68')
			st.plotly_chart(p1, use_container_width=True)


		with col2:
			#gráfico 2
			surv2 = model.predict_cumulative_hazard_function(single_sample, return_array=True)

			hazard = pd.DataFrame({'Hazard Acumulado': value for value in surv2})
			hazard['Meses'] = hazard.index+1

			hazard = hazard.head(faixa*12)	

			p2 = px.line(hazard,x='Meses',y='Hazard Acumulado', markers=False, title="Curva de de Hazard acumulada")
			p2.update_layout(autosize=True)
			p2.update_traces(line_color='#666a68')
			st.plotly_chart(p2, use_container_width=True)

		st.subheader('Sobrevida por anos')
		col3, col4, col5 = st.columns([5,5,5])
		
		with col3:
			st.metric(
				label='1 Ano',
				value="{:.2f}%".format(surv[0, 11] * 100),
			)	

		with col4:
			st.metric(
				label='3 Anos',
				value="{:.2f}%".format(surv[0, 36] * 100)
			)	

		with col5:
			st.metric(
				label='5 Anos',
				value="{:.2f}%".format(surv[0, 60] * 100)
			)
		
			
				
		
	st.subheader("Instruções:")
	st.write("1. Selecione as informações do pacientes no menu à esquerda\n2. Pressione o botão para Submeter\n3. O modela irá gerar a predição de sobrevida")
	st.write('***Nota: esse modelo é um projeto de pesquisa e sua acurácia não pode ser garantida!***')
