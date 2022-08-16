import joblib
import streamlit as st
import streamlit.components.v1 as stc 
import joblib
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

	st.title("Sistema de apoio à decisão para sobrevida de câncer de mama")

	st.subheader("Calculadora Online")

	form = st.form(key="annotation")

	with form:

		idade = st.number_input("Idade",1,100, value=54)
		estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
		tam_tumor = st.slider("Tamanho do tumor: ", min_value=1, max_value=150, value=24)
		estrog = st.radio("Estrogênio", ('Positivo','Negativo'))
		prog = st.radio("Progesterona", ('Positivo','Negativo'))


		submitted = st.form_submit_button(label="Submiter")

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
				
				st.write("Curva de probbilidade de sobrevivência")
				
				survival = pd.DataFrame({'Probabilidade de Sobrevivência': value for value in surv})
				survival['Meses'] = survival.index

				fig = plt.figure()
				sns.lineplot(survival['Meses'],survival['Probabilidade de Sobrevivência'], drawstyle='steps-pre')
				st.pyplot(fig)

			with col2:
				surv2 = model.predict_cumulative_hazard_function(single_sample, return_array=True)

				st.write("Predição da função de Hazard acumulada")
				hazard = pd.DataFrame({'Hazard Acumulado': value for value in surv2})
				hazard['Meses'] = hazard.index

				fig = plt.figure()
				sns.lineplot(hazard['Meses'],hazard['Hazard Acumulado'], drawstyle='steps-pre')
				st.pyplot(fig)

			
if __name__ == "__main__":
    main()