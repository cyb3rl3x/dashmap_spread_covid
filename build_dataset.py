import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Capitais e coordenadas
capitais = {
    "São Paulo": [-23.5505, -46.6333],
    "Rio de Janeiro": [-22.9068, -43.1729],
    "Fortaleza": [-3.7172, -38.5433],
    "Belo Horizonte": [-19.9167, -43.9345],
    "Brasília": [-15.7939, -47.8828],
    "Salvador": [-12.9777, -38.5016],
    "Curitiba": [-25.4284, -49.2733],
    "Manaus": [-3.1190, -60.0217],
    "Porto Alegre": [-30.0346, -51.2177],
    "Recife": [-8.0476, -34.8770],
    "Belém": [-1.4558, -48.4902],
    "São Luís": [-2.5307, -44.3068],
    "Maceió": [-9.6498, -35.7089],
    "João Pessoa": [-7.1153, -34.8610],
    "Teresina": [-5.0892, -42.8016],
    "Aracaju": [-10.9472, -37.0731],
    "Palmas": [-10.2128, -48.3602],
    "Campo Grande": [-20.4697, -54.6201],
    "Cuiabá": [-15.6014, -56.0979],
    "Boa Vista": [2.8238, -60.6753],
    "Macapá": [0.0349, -51.0694],
    "Porto Velho": [-8.7608, -63.8999],
    "Rio Branco": [-9.97499, -67.8243],
    "Vitória": [-20.3155, -40.3128],
    "Goiânia": [-16.6869, -49.2648],
    "Florianópolis": [-27.5954, -48.5480]
}

# Focos iniciais
focos = {
    "SP": capitais["São Paulo"],
    "RJ": capitais["Rio de Janeiro"],
    "Fortaleza": capitais["Fortaleza"]
}

np.random.seed(42)
n_frames = 50
pontos_capital = 120
pontos_dispersos = 60
dados = []

# Cálculo da capital mais próxima
capital_mais_proxima = {}
for cidade, coord in capitais.items():
    menor_dist = float("inf")
    foco_proximo = None
    for foco_nome, foco_coord in focos.items():
        dist = geodesic(coord, foco_coord).km
        if dist < menor_dist:
            menor_dist = dist
            foco_proximo = foco_nome
    capital_mais_proxima[cidade] = (foco_proximo, menor_dist)

# Normalização para tempo de início
distancias = [d for _, d in capital_mais_proxima.values()]
min_d, max_d = min(distancias), max(distancias)
capital_inicio_frame = {}
for cidade, (foco, dist) in capital_mais_proxima.items():
    if cidade in focos:
        capital_inicio_frame[cidade] = 0
    else:
        progresso = (dist - min_d) / (max_d - min_d)
        capital_inicio_frame[cidade] = int(5 + progresso * (n_frames - 15))

# Geração de dados
for frame in range(n_frames):
    data = pd.to_datetime("2020-03-01") + pd.to_timedelta(frame * 2, unit="D")
    
    for cidade, (lat, lon) in capitais.items():
        inicio = capital_inicio_frame[cidade]
        if frame < inicio:
            continue
        
        if cidade in focos:
            intensidade_base = 1.0
        else:
            progresso = (frame - inicio) / (n_frames - inicio)
            intensidade_base = min(progresso ** 1.5, 1.0)

        # 1. PONTOS NA CAPITAL (70%)
        for _ in range(pontos_capital):
            lat_ponto = lat + np.random.normal(0, 0.4)  # dispersão aumentada
            lon_ponto = lon + np.random.normal(0, 0.4)
            intensidade = np.clip(np.random.normal(loc=intensidade_base, scale=0.3), 0, 1)
            dados.append([data.strftime("%Y-%m-%d"), lat_ponto, lon_ponto, intensidade])

        # 2. PONTOS ENTRE ESTADOS (30%)
        foco, _ = capital_mais_proxima[cidade]
        lat_foco, lon_foco = focos[foco]
        for _ in range(pontos_dispersos):
            alpha = np.random.uniform(0.2, 0.9)  # ponto intermediário entre foco e capital
            lat_inter = (1 - alpha) * lat_foco + alpha * lat
            lon_inter = (1 - alpha) * lon_foco + alpha * lon
            lat_ponto = lat_inter + np.random.normal(0, 0.5)
            lon_ponto = lon_inter + np.random.normal(0, 0.5)
            intensidade = np.clip(np.random.normal(loc=intensidade_base * alpha, scale=0.25), 0, 1)
            dados.append([data.strftime("%Y-%m-%d"), lat_ponto, lon_ponto, intensidade])

# Criar DataFrame
df = pd.DataFrame(dados, columns=["data", "lat", "lon", "intensidade"])
df.to_csv("data/dataset_infeccao_brasil.csv", index=False)
