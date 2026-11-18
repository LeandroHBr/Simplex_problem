import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from simplex import simplex,exercice_query
df = pd.read_excel("tabela.xlsx")

exercices,score = exercice_query(df,["isquiotibiais"])
df_size = len(exercices)
nomes_exercicios = exercices["name"].to_numpy()
exercices_data = exercices.iloc[:, 15:32]
exercices_columns = exercices_data.columns.to_numpy()
exercices_data = exercices_data.to_numpy()



result = simplex(exercices,score,df_size,exercices_data,exercices_columns);
Tabela_resultado = []
n=0


for i in range(len(result)):
    if result[i].varValue > 0:
        n+=1
        Tabela_resultado.append ({ 
            "Exercício": exercices.iloc[i]["name"],
            "Séries": result[i].varValue
        })
df_final = pd.DataFrame(Tabela_resultado)
print(df_final)
print(n)