import dash
from dash import html
import os
import subprocess



# Verificações automáticas
if not os.path.exists("data/dataset_infeccao_brasil.csv"):
    subprocess.run(["python", "01_gerar_dados.py"], check=True)

if not os.path.exists("mapa_animado_infeccao.html"):
    subprocess.run(["python", "02_gerar_mapa.py"], check=True)


# Caminho para o arquivo do mapa gerado
MAP_FILE = "mapa_animado_infeccao.html"

# Verifica se o arquivo existe
if not os.path.exists(MAP_FILE):
    raise FileNotFoundError(f"O arquivo {MAP_FILE} não foi encontrado. Execute 02_gerar_mapa.py primeiro.")

# Lê o conteúdo HTML do mapa
with open(MAP_FILE, "r", encoding="utf-8") as f:
    mapa_html = f.read()

# Criação do app Dash
app = dash.Dash(__name__)
app.title = "Mapa de Infecção COVID-19"

# Layout
app.layout = html.Div([
    html.H1("Propagação Simulada da COVID-19 no Brasil", style={'textAlign': 'center'}),
    html.P("Animação da disseminação a partir de SP, RJ e Fortaleza com expansão para todo o país.",
           style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Iframe(srcDoc=mapa_html, width="100%", height="720", style={"border": "none"})
])

# Execução
if __name__ == "__main__":
    app.run(debug=True)
