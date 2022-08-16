from turtle import shape
import joblib
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
	page_icon="🏪",
	layout="wide"
)

def main():
	@st.cache(allow_output_mutation=True)
	def load_model(model_file):
		model = joblib.load(open(os.path.join(model_file),"rb"))
		return model

	model = load_model('model/rsf_2022.pkl')

	st.markdown("<h1 style='text-align: center; color:#666a68;'>Predição de Sobrevida para Câncer de Mama</h1>", unsafe_allow_html=True)

	st.markdown("<h2 style='text-align: center; color: #989e9a;'>Selecione as informações abaixo para realizar a predição de sobrevida</h2>", unsafe_allow_html=True)

	form = st.form(key="annotation")

	with form:
		col1,col2 = st.columns(2)

		with col1:
			idade = st.number_input("Idade",1,100, value=54)
			prog = st.radio("Progesterona", ('Positivo','Negativo'))

		with col2:	
			estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
			estrog = st.radio("Estrogênio", ('Positivo','Negativo'))
			

		tam_tumor = st.slider("Tamanho do tumor: ", min_value=1, max_value=150, value=24)
		faixa = st.slider("Escolha quantos anos de visualização:", min_value=3, max_value=10, value=5)

		submitted = st.form_submit_button(label="Submeter")
	
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

			col1,col2 = st.columns(2)

			with col1:

				surv = model.predict_survival_function(single_sample, return_array=True)
				
				survival = pd.DataFrame({'Probabilidade de Sobrevivência': value for value in surv})
				survival['Meses'] = survival.index+1

				survival = survival.head(faixa)

				p1 = px.line(survival,x='Meses',y='Probabilidade de Sobrevivência', markers=True, title="Curva de probbilidade de sobrevivência")
				p1.update_traces(line_color='#666a68')
				st.plotly_chart(p1)

			with col2:
				surv2 = model.predict_cumulative_hazard_function(single_sample, return_array=True)

				hazard = pd.DataFrame({'Hazard Acumulado': value for value in surv2})
				hazard['Meses'] = hazard.index+1

				hazard = hazard.head(faixa)	

				p2 = px.line(hazard,x='Meses',y='Hazard Acumulado', markers=True, title="Predição da função de Hazard acumulada")
				p2.update_traces(line_color='#666a68')
				st.plotly_chart(p2)
			
if __name__ == "__main__":
    main()