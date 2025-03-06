import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash_bootstrap_components import themes

# ========== Dados Simulados ==========
# Dados de jogadores
players = pd.DataFrame({
    'Jogador': ['Faker', 'Caps', 'Rookie', 'Knight', 'ShowMaker'],
    'KDA': [5.8, 4.2, 6.1, 5.3, 4.9],
    'Dano/Min': [650, 580, 720, 630, 590],
    'CS/Min': [8.5, 7.9, 9.2, 8.7, 8.1],
    'Campeões': ['LeBlanc, Azir, Ryze', 'Syndra, Orianna, Corki', 
                 'Zoe, Akali, Sylas', 'Twisted Fate, Galio, Lucian',
                 'Zed, Yasuo, Irelia']
})

# Dados de partidas
matches = pd.DataFrame({
    'MatchID': [1, 2, 3],
    'Time1': ['T1', 'G2', 'IG'],
    'Time2': ['DK', 'RNG', 'FPX'],
    'Mapa': ['Summoners Rift', 'Howling Abyss', 'Summoners Rift'],
    'Duração': ['32:15', '28:40', '37:20']
})

# Dados táticos (heatmap)
np.random.seed(42)
tactical_data = pd.DataFrame({
    'x': np.random.randint(0, 100, 200),
    'y': np.random.randint(0, 100, 200),
    'Intensidade': np.random.rand(200)
})

# Previsão de resultados
prediction_data = pd.DataFrame({
    'Time': ['T1', 'DK', 'G2', 'RNG'],
    'Win Probability': [78, 65, 82, 58]
})

# ========== Layout do Dashboard ==========
app = dash.Dash(__name__, external_stylesheets=[themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1("eSports Analytics Dashboard", 
               style={'color': 'white', 'margin': '20px'}),
    ], className='bg-dark rounded'),
    
    # Linha de Status em Tempo Real
    html.Div([
        html.Div([
            html.H4("Partidas Ativas", className="text-success"),
            html.H2("3", id="live-matches", className="display-4")
        ], className="card-body text-center bg-light m-2 rounded"),
        
        html.Div([
            html.H4("Jogadores Online", className="text-primary"),
            html.H2("127", id="live-players", className="display-4")
        ], className="card-body text-center bg-light m-2 rounded"),
        
        html.Div([
            html.H4("Eventos/Min", className="text-danger"),
            html.H2("48", id="events-min", className="display-4")
        ], className="card-body text-center bg-light m-2 rounded"),
    ], className="d-flex justify-content-around"),
    
    # Seleção de Partida
    html.Div([
        dcc.Dropdown(
            id='match-selector',
            options=[{'label': f"{row['Time1']} vs {row['Time2']}", 'value': row['MatchID']} 
                    for _, row in matches.iterrows()],
            value=1,
            className='m-3'
        )
    ]),
    
    # Gráficos Principais
    html.Div([
        html.Div([
            dcc.Graph(id='tactical-heatmap'),
            dcc.Interval(id='live-update', interval=5000, n_intervals=0)
        ], className='col-md-8'),
        
        html.Div([
            dcc.Graph(id='player-stats'),
            dcc.Graph(id='win-prediction')
        ], className='col-md-4')
    ], className='row'),
    
    # Tabelas Comparativas
    html.Div([
        dash_table.DataTable(
            id='team-comparison',
            columns=[{"name": i, "id": i} for i in ['Estatística', 'Time1', 'Time2']],
            style_table={'overflowX': 'auto'},
            className='m-3'
        )
    ])
], className='container')

# ========== Callbacks ==========
@app.callback(
    [Output('tactical-heatmap', 'figure'),
     Output('player-stats', 'figure'),
     Output('win-prediction', 'figure'),
     Output('team-comparison', 'data')],
    [Input('match-selector', 'value'),
     Input('live-update', 'n_intervals')]
)
def update_dashboard(selected_match, n):
    # Heatmap Tático Atualizado
    tactical_fig = px.density_heatmap(
        tactical_data, x='x', y='y', 
        title='Mapa Tático - Posicionamento dos Jogadores',
        color_continuous_scale='Viridis'
    )
    
    # Estatísticas dos Jogadores
    player_fig = px.bar(
        players, x='Jogador', y='KDA',
        title='Performance dos Jogadores (KDA)',
        color='Dano/Min'
    )
    
    # Previsão de Resultados
    prediction_fig = px.pie(
        prediction_data, names='Time', values='Win Probability',
        title='Probabilidade de Vitória',
        hole=0.4
    )
    
    # Dados Comparativos dos Times
    selected_match_data = matches[matches['MatchID'] == selected_match].iloc[0]
    comparison_data = [
        {'Estatística': 'KDA Médio', 'Time1': 4.8, 'Time2': 5.1},
        {'Estatística': 'Dano/Min', 'Time1': 620, 'Time2': 590},
        {'Estatística': 'Objetivos', 'Time1': 3, 'Time2': 2}
    ]
    
    return tactical_fig, player_fig, prediction_fig, comparison_data

# ========== Executar o App ==========
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
