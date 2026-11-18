import pandas as pd
import pulp


df = pd.read_excel("tabela.xlsx")

def exercice_query(df, exercices,level):
    score = []
    
    exercices_data = df[
        (df["primaryMuscles"].isin(exercices) | 
        df["secondaryMuscles"].astype(str).str.lower().apply(
            lambda x: any(ex in x for ex in exercices))) &
        df["category"].isin(["powerlifting","forca"]) &
        df["level"].isin(level)
    ]
    
    for index, row in exercices_data.iterrows():
        x = 0
        for col in exercices:
            if col in row:
                x += row[col]
        score.append(x)
        
    # Se quiser salvar o score de volta no dataframe:
    
    print(score)
    
    return exercices_data,score

#exercices,score = exercice_query(df,["isquiotibiais"])
#df_size = len(exercices)
#nomes_exercicios = exercices["name"].to_numpy()
#exercices_data = exercices.iloc[:, 15:32]
#exercices_columns = exercices_data.columns.to_numpy()
#exercices_data = exercices_data.to_numpy()


def simplex(exercices,score,df_size,exercices_data,exercices_columns,SERIES_DISPONÍVEIS,max_exercicios,tempo_de_busca):
    modelo = pulp.LpProblem("Otimizacao_Treino_Hipertrofia", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x_{i}", lowBound=0,upBound=5, cat='Integer') for i in range(df_size)]
    y = [pulp.LpVariable(f"y_{i}", cat='Binary') for i in range(df_size)]
    modelo += pulp.lpSum(score[i] * x[i] for i in range(df_size)), "Maximizar_Score_Total"
    MAX_ESTIMULO_POR_MUSCULO = [25,20,16,20,26,26,22,25,20,16,12,18,26,14,16,16,16]
    musculo = 0

    for m in exercices_columns:
        modelo += pulp.lpSum(exercices_data[i, musculo] * x[i] for i in range(df_size)) <= MAX_ESTIMULO_POR_MUSCULO[musculo]
        musculo +=1;
        
    for i in range(df_size):
        # Se o exercício entrou (y=1), x deve ser no mínimo 3 séries
        modelo += x[i] >= 3 * y[i], f"Min_Series_{i}"
        # Se o exercício entrou, x não pode passar de 5 séries (por exemplo). Se y=0, x força a ser 0.
        modelo += x[i] <= 10 * y[i], f"Max_Series_{i}"
    #escolhe no máximo 5 exercícios
    modelo += pulp.lpSum(y[i] for i in range(df_size)) <= max_exercicios
    #limitação de séries disponíveis com base no tempo
    modelo += pulp.lpSum(x[i] for i in range(df_size)) <= SERIES_DISPONÍVEIS
    modelo.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=tempo_de_busca))

    return x
#x = simplex();

"""n = 0;
for i in range(df_size):
    if x[i].varValue > 0:
        n+=1
        print(f"exercício:{nomes_exercicios[i]}\nseries: {x[i].varValue}")
        
        
print(n)

"""