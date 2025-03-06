import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Geração de dados fictícios para o dashboard
def generate_fake_data():
    # Datas (últimos 30 dias)
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    dates.reverse()
    dates_str = [date.strftime('%Y-%m-%d') for date in dates]
    
    # Plataformas
    platforms = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn']
    
    # Seguidores
    followers_data = []
    for platform in platforms:
        base = random.randint(5000, 20000)
        growth_rate = random.uniform(0.005, 0.015)
        followers = [int(base * (1 + growth_rate) ** i) for i in range(30)]
        for i, date in enumerate(dates_str):
            followers_data.append({
                'date': date,
                'platform': platform,
                'followers': followers[i]
            })
    followers_df = pd.DataFrame(followers_data)
    
    # Engajamento
    engagement_data = []
    for platform in platforms:
        for date in dates_str:
            engagement_data.append({
                'date': date,
                'platform': platform,
                'likes': random.randint(100, 1000),
                'comments': random.randint(10, 100),
                'shares': random.randint(5, 50)
            })
    engagement_df = pd.DataFrame(engagement_data)
    
    # Sentimento
    sentiment_data = []
    for platform in platforms:
        total = 100
        positive = random.randint(40, 70)
        negative = random.randint(5, 20)
        neutral = total - positive - negative
        sentiment_data.append({
            'platform': platform,
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        })
    sentiment_df = pd.DataFrame(sentiment_data)
    
    # Dados demográficos
    demographics_data = []
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    genders = ['Masculino', 'Feminino', 'Outro']
    
    for platform in platforms:
        for age in age_groups:
            for gender in genders:
                demographics_data.append({
                    'platform': platform,
                    'age_group': age,
                    'gender': gender,
                    'percentage': random.uniform(1, 10)
                })
    demographics_df = pd.DataFrame(demographics_data)
    
    # Dados geográficos
    countries = ['Brasil', 'EUA', 'Portugal', 'México', 'Argentina', 'Colômbia', 'Reino Unido', 'Espanha', 'França', 'Alemanha']
    geo_data = []
    for platform in platforms:
        remaining = 100
        for country in countries[:-1]:
            value = random.randint(1, remaining - len(countries) + len(geo_data) + 1)
            remaining -= value
            geo_data.append({
                'platform': platform,
                'country': country,
                'users': value
            })
        geo_data.append({
            'platform': platform,
            'country': countries[-1],
            'users': remaining
        })
    geo_df = pd.DataFrame(geo_data)
    
    # Palavras populares para a nuvem de palavras
    words = ["conteúdo", "social", "marketing", "digital", "marca", "engajamento", "seguidores", 
             "campanha", "viral", "trending", "hashtag", "influenciador", "alcance", "conversão", 
             "ROI", "SEO", "compartilhamento", "publicação", "visualizações", "fãs", "cliques", 
             "comentários", "likes", "comunicação", "audiência", "plataforma", "estratégia"]
    
    word_data = {}
    for word in words:
        word_data[word] = random.randint(10, 100)
        
    return followers_df, engagement_df, sentiment_df, demographics_df, geo_df, word_data

# Gerar os dados
followers_df, engagement_df, sentiment_df, demographics_df, geo_df, word_data = generate_fake_data()

# Iniciar o app Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Definir cores para o tema
colors = {
    'background': '#f9f9f9',
    'text': '#333333',
    'plot_bg': '#ffffff',
    'grid': '#e0e0e0',
    'instagram': '#E1306C',
    'facebook': '#4267B2',
    'twitter': '#1DA1F2',
    'linkedin': '#0077B5',
}

# Define uma função para criar a nuvem de palavras
def create_wordcloud(word_data):
    wc = WordCloud(background_color="white", width=800, height=400, max_words=100)
    wc.generate_from_frequencies(word_data)
    
    # Converte a imagem para base64 para exibir no Dash
    img = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

# Layout do Dashboard
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    # Cabeçalho
    html.Div([
        html.H1("Dashboard de Mídias Sociais", style={'textAlign': 'center', 'color': colors['text']}),
        html.P("Análise de performance de perfis e campanhas em redes sociais", style={'textAlign': 'center', 'color': colors['text']}),
    ]),
    
    # Filtros
    html.Div([
        html.H3("Filtros", style={'color': colors['text']}),
        html.Div([
            html.Label("Plataforma"),
            dcc.Dropdown(
                id='platform-filter',
                options=[{'label': platform, 'value': platform} for platform in ['Todas', 'Instagram', 'Facebook', 'Twitter', 'LinkedIn']],
                value='Todas',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Período"),
            dcc.Dropdown(
                id='period-filter',
                options=[
                    {'label': 'Últimos 7 dias', 'value': '7'},
                    {'label': 'Últimos 14 dias', 'value': '14'},
                    {'label': 'Últimos 30 dias', 'value': '30'}
                ],
                value='30',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px', 'marginBottom': '20px'}),
    
    # Visão geral (KPIs)
    html.Div([
        html.H3("Visão Geral", style={'color': colors['text']}),
        html.Div([
            # Métricas resumidas em cartões
            html.Div([
                html.H4("Total de Seguidores"),
                html.H2(id='total-followers', style={'color': '#4C78A8'})
            ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '10px', 'borderRadius': '5px', 'margin': '0 1%', 'textAlign': 'center'}),
            
            html.Div([
                html.H4("Engajamento Total"),
                html.H2(id='total-engagement', style={'color': '#72B7B2'})
            ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '10px', 'borderRadius': '5px', 'margin': '0 1%', 'textAlign': 'center'}),
            
            html.Div([
                html.H4("Taxa Média de Conversão"),
                html.H2(id='avg-conversion-rate', style={'color': '#F58518'})
            ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '10px', 'borderRadius': '5px', 'margin': '0 1%', 'textAlign': 'center'}),
            
            html.Div([
                html.H4("Sentimento Positivo"),
                html.H2(id='positive-sentiment', style={'color': '#54A24B'})
            ], className='metric-card', style={'width': '23%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '10px', 'borderRadius': '5px', 'margin': '0 1%', 'textAlign': 'center'}),
        ]),
    ], style={'marginBottom': '20px'}),
    
    # Linha 1 de gráficos
    html.Div([
        # Crescimento de seguidores
        html.Div([
            html.H3("Crescimento de Seguidores", style={'color': colors['text']}),
            dcc.Graph(id='followers-growth'),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px'}),
        
        # Análise de engajamento
        html.Div([
            html.H3("Análise de Engajamento", style={'color': colors['text']}),
            dcc.Graph(id='engagement-analysis'),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px', 'float': 'right'}),
    ], style={'marginBottom': '20px'}),
    
    # Linha 2 de gráficos
    html.Div([
        # Análise de sentimento
        html.Div([
            html.H3("Análise de Sentimento", style={'color': colors['text']}),
            dcc.Graph(id='sentiment-analysis'),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px'}),
        
        # Demografia do público
        html.Div([
            html.H3("Demografia do Público", style={'color': colors['text']}),
            dcc.Graph(id='audience-demographics'),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px', 'float': 'right'}),
    ], style={'marginBottom': '20px'}),
    
    # Linha 3 de gráficos
    html.Div([
        # Distribuição geográfica
        html.Div([
            html.H3("Distribuição Geográfica", style={'color': colors['text']}),
            dcc.Graph(id='geographic-distribution'),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px'}),
        
        # Nuvem de palavras
        html.Div([
            html.H3("Temas Populares", style={'color': colors['text']}),
            html.Img(id='wordcloud-image', style={'width': '100%'}),
        ], style={'width': '49%', 'display': 'inline-block', 'backgroundColor': colors['plot_bg'], 'padding': '15px', 'borderRadius': '5px', 'float': 'right'}),
    ], style={'marginBottom': '20px'}),
    
    # Rodapé
    html.Div([
        html.P("Dados atualizados em: " + datetime.now().strftime("%d/%m/%Y %H:%M"), style={'textAlign': 'center', 'color': colors['text']}),
    ], style={'marginTop': '30px'})
])

# Callbacks para atualizar os gráficos e métricas

# Callback para o total de seguidores
@app.callback(
    Output('total-followers', 'children'),
    [Input('platform-filter', 'value'),
     Input('period-filter', 'value')]
)
def update_total_followers(platform, period):
    filtered_df = followers_df
    
    # Filtra por período
    period = int(period)
    latest_dates = sorted(filtered_df['date'].unique())[-period:]
    filtered_df = filtered_df[filtered_df['date'].isin(latest_dates)]
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Obtém os últimos valores de seguidores para cada plataforma
    latest_date = max(filtered_df['date'])
    latest_followers = filtered_df[filtered_df['date'] == latest_date]
    
    total = latest_followers['followers'].sum()
    return f"{total:,}".replace(",", ".")

# Callback para engajamento total
@app.callback(
    Output('total-engagement', 'children'),
    [Input('platform-filter', 'value'),
     Input('period-filter', 'value')]
)
def update_total_engagement(platform, period):
    filtered_df = engagement_df
    
    # Filtra por período
    period = int(period)
    latest_dates = sorted(filtered_df['date'].unique())[-period:]
    filtered_df = filtered_df[filtered_df['date'].isin(latest_dates)]
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Soma likes, comentários e compartilhamentos
    total_engagement = filtered_df['likes'].sum() + filtered_df['comments'].sum() + filtered_df['shares'].sum()
    
    return f"{total_engagement:,}".replace(",", ".")

# Callback para taxa média de conversão (fictício - seria baseado em dados reais)
@app.callback(
    Output('avg-conversion-rate', 'children'),
    [Input('platform-filter', 'value'),
     Input('period-filter', 'value')]
)
def update_conversion_rate(platform, period):
    # Em um cenário real, este seria calculado com dados reais de conversão
    # Para este exemplo, geramos um valor aleatório
    if platform == 'Todas':
        rate = random.uniform(1.5, 3.0)
    else:
        platform_rates = {
            'Instagram': random.uniform(2.0, 3.5),
            'Facebook': random.uniform(1.8, 3.0),
            'Twitter': random.uniform(1.0, 2.5),
            'LinkedIn': random.uniform(2.2, 4.0)
        }
        rate = platform_rates[platform]
    
    return f"{rate:.2f}%".replace(".", ",")

# Callback para sentimento positivo
@app.callback(
    Output('positive-sentiment', 'children'),
    [Input('platform-filter', 'value')]
)
def update_positive_sentiment(platform):
    filtered_df = sentiment_df
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Calcula média de sentimento positivo
    avg_positive = filtered_df['positive'].mean()
    
    return f"{avg_positive:.1f}%".replace(".", ",")

# Callback para o gráfico de crescimento de seguidores
@app.callback(
    Output('followers-growth', 'figure'),
    [Input('platform-filter', 'value'),
     Input('period-filter', 'value')]
)
def update_followers_growth(platform, period):
    filtered_df = followers_df
    
    # Filtra por período
    period = int(period)
    latest_dates = sorted(filtered_df['date'].unique())[-period:]
    filtered_df = filtered_df[filtered_df['date'].isin(latest_dates)]
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Cria o gráfico
    fig = px.line(filtered_df, x='date', y='followers', color='platform',
                 color_discrete_map={
                     'Instagram': colors['instagram'],
                     'Facebook': colors['facebook'],
                     'Twitter': colors['twitter'],
                     'LinkedIn': colors['linkedin']
                 })
    
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['plot_bg'],
        font_color=colors['text'],
        xaxis_title="Data",
        yaxis_title="Número de Seguidores",
        legend_title="Plataforma",
        hovermode="x unified"
    )
    
    return fig

# Callback para análise de engajamento
@app.callback(
    Output('engagement-analysis', 'figure'),
    [Input('platform-filter', 'value'),
     Input('period-filter', 'value')]
)
def update_engagement_analysis(platform, period):
    filtered_df = engagement_df
    
    # Filtra por período
    period = int(period)
    latest_dates = sorted(filtered_df['date'].unique())[-period:]
    filtered_df = filtered_df[filtered_df['date'].isin(latest_dates)]
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Agrupa por plataforma
    platform_engagement = filtered_df.groupby('platform').agg({
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum'
    }).reset_index()
    
    # Melta os dados para o formato adequado
    melted_df = pd.melt(platform_engagement, id_vars=['platform'], value_vars=['likes', 'comments', 'shares'],
                        var_name='engagement_type', value_name='count')
    
    # Mapeamento para nomes em português
    engagement_map = {
        'likes': 'Curtidas',
        'comments': 'Comentários',
        'shares': 'Compartilhamentos'
    }
    melted_df['engagement_type'] = melted_df['engagement_type'].map(engagement_map)
    
    # Cria o gráfico
    fig = px.bar(melted_df, x='platform', y='count', color='engagement_type', barmode='group',
                color_discrete_sequence=px.colors.qualitative.Set1)
    
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['plot_bg'],
        font_color=colors['text'],
        xaxis_title="Plataforma",
        yaxis_title="Quantidade",
        legend_title="Tipo de Engajamento",
        hovermode="closest"
    )
    
    return fig

# Callback para análise de sentimento
@app.callback(
    Output('sentiment-analysis', 'figure'),
    [Input('platform-filter', 'value')]
)
def update_sentiment_analysis(platform):
    filtered_df = sentiment_df
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Melta os dados para o formato adequado
    melted_df = pd.melt(filtered_df, id_vars=['platform'], value_vars=['positive', 'neutral', 'negative'],
                        var_name='sentiment', value_name='percentage')
    
    # Mapeamento para nomes em português
    sentiment_map = {
        'positive': 'Positivo',
        'neutral': 'Neutro',
        'negative': 'Negativo'
    }
    melted_df['sentiment'] = melted_df['sentiment'].map(sentiment_map)
    
    # Cria o gráfico
    fig = px.pie(melted_df, values='percentage', names='sentiment', facet_col='platform',
                color='sentiment', color_discrete_map={
                    'Positivo': '#54A24B',
                    'Neutro': '#EECA3B',
                    'Negativo': '#E45756'
                })
    
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['plot_bg'],
        font_color=colors['text'],
        legend_title="Sentimento",
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    return fig

# Callback para demografia do público
@app.callback(
    Output('audience-demographics', 'figure'),
    [Input('platform-filter', 'value')]
)
def update_audience_demographics(platform):
    filtered_df = demographics_df
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    
    # Agrupa por faixa etária e gênero
    grouped_df = filtered_df.groupby(['platform', 'age_group', 'gender']).agg({
        'percentage': 'sum'
    }).reset_index()
    
    # Cria o gráfico
    fig = px.bar(grouped_df, x='age_group', y='percentage', color='gender', barmode='group',
                facet_col='platform', color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['plot_bg'],
        font_color=colors['text'],
        xaxis_title="Faixa Etária",
        yaxis_title="Porcentagem",
        legend_title="Gênero",
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    return fig

# Callback para distribuição geográfica
@app.callback(
    Output('geographic-distribution', 'figure'),
    [Input('platform-filter', 'value')]
)
def update_geographic_distribution(platform):
    filtered_df = geo_df
    
    # Filtra por plataforma
    if platform != 'Todas':
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    else:
        # Se 'Todas' for selecionado, agrupe os dados por país
        filtered_df = filtered_df.groupby('country').agg({
            'users': 'sum'
        }).reset_index()
    
    # Cria o gráfico
    if platform != 'Todas':
        fig = px.choropleth(filtered_df, locations='country', locationmode='country names',
                          color='users', hover_name='country', facet_col='platform',
                          color_continuous_scale=px.colors.sequential.Blues)
    else:
        fig = px.choropleth(filtered_df, locations='country', locationmode='country names',
                          color='users', hover_name='country',
                          color_continuous_scale=px.colors.sequential.Blues)
    
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['plot_bg'],
        font_color=colors['text'],
        margin=dict(t=30, b=30, l=30, r=30),
        height=400
    )
    
    if platform != 'Todas':
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    return fig

# Callback para nuvem de palavras
@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('platform-filter', 'value')]
)
def update_wordcloud(platform):
    # Em um cenário real, poderíamos filtrar as palavras por plataforma
    # Aqui, estamos retornando a mesma nuvem de palavras
    return create_wordcloud(word_data)

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)