import joblib
import streamlit as st
import streamlit.components.v1 as stc 
import joblib
import os
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
	page_title="App Predição de Sobrevida",
	page_icon="🏪",
	layout="wide"
)

def main():
	@st.cache
	def load_model(model_file):
		model = joblib.load(open(os.path.join(model_file),"rb"))
		return model

	model = load_model('model/rsf_2022.pkl')
	
	st.title("Sistema de apoio à decisão para sobrevida de câncer de mama")

	st.subheader("Calculadora Online")

	form = st.form(key="annotation")

	with form:

		idade = st.number_input("Idade",10,100, value=54)
		estadiamento = st.selectbox("Estadiamento",("IIA","IIB", "IIIA", "IIIB", "IIIC"))
		tam_tumor = st.number_input("Tamanho do tumor", 20,150, value=24)
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

	if submitted:
		with st.expander("Curvas de probabilidade de sobrevivência"):

			single_sample = np.array(encoded_result).reshape(1,-1)

			
			prediction = model.predict(single_sample)
			col1,col2 = st.columns(2)

			with col1:
				surv = model.predict_survival_function(single_sample, return_array=True)

				st.write("Curva de sobrevivência")
				for i, s in enumerate(surv):
					plt.step(model.event_times_, s, where="post", label=str(i))
				plt.ylabel("Survival probability")
				plt.xlabel("Time in months")
				plt.legend()
				plt.grid(True)
			
			with col2:
				surv = model.predict_cumulative_hazard_function(single_sample, return_array=True)

				st.write("Predição da função de Hazard acumulada")
				for i, s in enumerate(surv):
					plt.step(model.event_times_, s, where="post", label=str(i))
				plt.ylabel("Cumulative hazard")
				plt.xlabel("Time in days")
				plt.legend()
				plt.grid(True)

if __name__ == "__main__":
    main()