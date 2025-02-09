from flask import Flask, render_template, request
import pandas as pd
import matplotlib

# Estava dando problema ao gerar o gráfico então essa linha manda o matplotlib gerar o gráfico no back-end e apenas exibir no front.
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)

# Carregar os dados
table = pd.read_csv("Preços semestrais - AUTOMOTIVOS_2024.01.csv", sep=";")
table.columns = table.columns.str.replace(" ", "_").str.strip()

#Converte o tipo da data
table["Data_da_Coleta"] = pd.to_datetime(table["Data_da_Coleta"], dayfirst=True)

combustiveis = ["Gasolina", "Diesel", "Etanol", "Gasolina Aditivada"]

@app.route("/")
def escolher_combustivel():
    return render_template("combustivel.html", combustiveis=combustiveis)

@app.route("/combustivel/<tipo>")
def listar_cidades(tipo):
    mapa_combustivel = {
        "Gasolina": "GASOLINA",
        "Diesel": "DIESEL",
        "Etanol": "ETANOL",
        "Gasolina Aditivada": "GASOLINA ADITIVADA"
    }

    if tipo not in mapa_combustivel:
        return "Combustível inválido!", 404

    df_filtrado = table[table["Produto"] == mapa_combustivel[tipo]]
    municipios = sorted(df_filtrado["Municipio"].unique())

    return render_template("index.html", municipios=municipios, tipo=tipo)

@app.route("/cidade/<tipo>/<municipio>")
def escolher_mes(tipo, municipio):
    df_cidade = table[(table["Municipio"] == municipio)]
    
    # Obter os meses disponíveis na tabela
    meses_disponiveis = sorted(df_cidade["Data_da_Coleta"].dt.strftime('%Y-%m').unique(), reverse=True)

    return render_template("mes.html", municipio=municipio, tipo=tipo, meses=meses_disponiveis)

@app.route("/cidade/<tipo>/<municipio>/<mes>")
def mostrar_grafico(tipo, municipio, mes):
    mapa_combustivel = {
        "Gasolina": "GASOLINA",
        "Diesel": "DIESEL",
        "Etanol": "ETANOL",
        "Gasolina Aditivada": "GASOLINA ADITIVADA"
    }

    df_cidade = table[(table["Municipio"] == municipio) & 
                      (table["Produto"] == mapa_combustivel[tipo]) &
                      (table["Data_da_Coleta"].dt.strftime('%Y-%m') == mes)]

    if df_cidade.empty:
        return f"Não há dados para {tipo} em {municipio} no mês {mes}.", 404

    plt.figure(figsize=(8, 4))
    plt.xlabel("Data")
    plt.ylabel("Preço (R$)")
    plt.title(f"{tipo} em {municipio} - {mes}")
    plt.xticks(rotation=45)

    #Desenha a Barra
    plt.bar(df_cidade["Data_da_Coleta"], df_cidade["Valor_de_Venda"], color="red")

    #Desenha a linha de destaque da barra
    plt.plot(df_cidade["Data_da_Coleta"], df_cidade["Valor_de_Venda"], marker="o", linestyle="--", color="black")

    # Converter o gráfico para base64.
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template("cidade.html", municipio=municipio, tipo=tipo, graph_url=graph_url, mes=mes)

if __name__ == "__main__":
    app.run(debug=True)
