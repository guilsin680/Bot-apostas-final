import requests
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import pickle

def carregar_modelo():
    if os.path.exists("modelo.pkl"):
        with open("modelo.pkl", "rb") as f:
            return pickle.load(f)
    return treinar_modelo()

def treinar_modelo():
    df = pd.read_csv("historico.csv")
    X = df[["home_goals", "away_goals"]]
    y = df["result"]
    model = RandomForestClassifier()
    model.fit(X, y)
    with open("modelo.pkl", "wb") as f:
        pickle.dump(model, f)
    return model

def buscar_jogos_hoje():
    key = os.getenv("API_FOOTBALL_KEY")
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": key}
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    params = {"date": data_hoje, "timezone": "America/Sao_Paulo"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()["response"]

def prever_jogos_hoje():
    jogos = buscar_jogos_hoje()
    modelo = carregar_modelo()
    mensagens = []

    for jogo in jogos:
        home = jogo["teams"]["home"]["name"]
        away = jogo["teams"]["away"]["name"]
        league = jogo["league"]["name"]
        date = jogo["fixture"]["date"]
        horario = datetime.fromisoformat(date[:-1]).strftime("%d/%m %H:%M")

        exemplo = np.array([[1, 2]])
        previsao = modelo.predict(exemplo)[0]
        prob = max(modelo.predict_proba(exemplo)[0])

        msg = f"**{league}**\n{horario} - {home} x {away}\nPrevisão: *{previsao}* (Confiança: {prob:.2%})"
        mensagens.append(msg)

    return mensagens
