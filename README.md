# Sistema de Apoio à Decisão para Sobrevida de Pacientes com Câncer de Mama 

Projeto em desenvolvimento realizado para o trabalho de conclusão de curso da graduação de Engenharia Biomédica na UFABC.

Esse aplicativo está sendo desenvolvido em python no VSCode e utiliza o framework Streamlit. 

O modelo utilizado foi o Randon Survival Forest (https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.ensemble.RandomSurvivalForest.html).

O modelo de Random Forest tem a capacidade de incorporar uma relação complexa e não linear entre as variáveis preditoras e a variável resposta, lidando facilmente com um conjunto de dados grande. A predição final é uma combinação das predições geradas em cada árvore de decisão obtida durante o processo, sendo cada árvore gerada ligeiramente diferente. Como saída da RSF, em cada nó final da árvore é feito uma previsão chamada de índice de risco de mortalidade (RM). Um RM alto significa um maior risco de o desfecho estudado acontecer, podendo ser morte, reincidência de uma doença ou expressão de um gene, por exemplo. Assim o RM é um número único que pode ser usado para colocar as pessoas em categorias de baixo, médio ou alto risco, por exemplo (Taylor, 2011). Outra característica é que a estrutura da árvore de sobrevivência impõe a hipótese nula de que o índice de sobrevivência é semelhante dentro de seus nós terminais, ou seja, indivíduos em um mesmo nó terminal compartilham um risco estimado comum.

