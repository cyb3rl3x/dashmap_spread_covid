import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

# Carrega o dataset
df = pd.read_csv("data/dataset_infeccao_brasil.csv")

# Organiza os dados em frames
datas = sorted(df['data'].unique())
heat_data = []

for data in datas:
    frame_df = df[df['data'] == data]
    frame = frame_df[['lat', 'lon', 'intensidade']].values.tolist()
    heat_data.append(frame)

# Criação do mapa
m = folium.Map(location=[-15.0, -47.0], zoom_start=4, tiles='cartodbpositron')

HeatMapWithTime(
    data=heat_data,
    index=datas,
    auto_play=True,
    max_opacity=0.85,
    radius=25,
    use_local_extrema=False
).add_to(m)

# Salvar como HTML
m.save("mapa_animado_infeccao.html")
m