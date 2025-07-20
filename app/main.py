# Streaming Platforms Interactive Dashboard
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Streaming Platforms Analysis Dashboard"

# Load and prepare data
def load_data():
    """Load and preprocess the streaming data"""
    df = pd.read_csv('../datasets/cleaned/movies_cleaned.csv')
    
    # Helper functions for JSON parsing
    def extract_country_names(countries_json):
        try:
            if pd.isna(countries_json) or countries_json == '[]':
                return []
            countries = json.loads(countries_json)
            return [country['name'] for country in countries]
        except:
            return []
    
    def extract_language_names(languages_json):
        try:
            if pd.isna(languages_json) or languages_json == '[]':
                return []
            languages = json.loads(languages_json)
            return [lang['name'] for lang in languages]
        except:
            return []
    
    # Apply parsing functions
    df['country_names'] = df['production_countries'].apply(extract_country_names)
    df['language_names'] = df['spoken_languages'].apply(extract_language_names)
    
    # Create expanded dataframes
    countries_expanded = []
    for idx, row in df.iterrows():
        for country in row['country_names']:
            new_row = row.copy()
            new_row['country'] = country
            countries_expanded.append(new_row)
    
    countries_df = pd.DataFrame(countries_expanded)
    
    # Add date parsing
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_month'] = df['release_date'].dt.month
    df['release_year'] = df['release_date'].dt.year
    
    return df, countries_df

# Load data
df, countries_df = load_data()
platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🎬 Streaming Platforms Analysis Dashboard", 
                className="header-title"),
        html.P("Interactive analysis of Netflix, Hulu, Prime Video, and Disney+ content libraries",
               className="header-subtitle")
    ], className="header"),
    
    # Main content
    html.Div([
        # Controls Section
        html.Div([
            html.H3("🎛️ Dashboard Controls"),
            
            # Platform selector
            html.Div([
                html.Label("Select Platforms:", className="control-label"),
                dcc.Checklist(
                    id='platform-selector',
                    options=[{'label': platform, 'value': platform} for platform in platforms],
                    value=platforms,  # All selected by default
                    className="platform-checklist"
                )
            ], className="control-group"),
            
            # Year range slider
            html.Div([
                html.Label("Select Year Range:", className="control-label"),
                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[df['Year'].min(), df['Year'].max()],
                    marks={year: str(year) for year in range(df['Year'].min(), df['Year'].max()+1, 5)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], className="control-group"),
            
            # Rating range slider
            html.Div([
                html.Label("Select Rating Range:", className="control-label"),
                dcc.RangeSlider(
                    id='rating-slider',
                    min=0,
                    max=10,
                    value=[0, 10],
                    step=0.5,
                    marks={i: f'{i}' for i in range(0, 11, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], className="control-group")
        ], className="controls-panel"),
        
        # Dashboard content
        html.Div([
            # Key Metrics Row
            html.Div([
                html.H3("📊 Key Metrics"),
                html.Div(id="key-metrics", className="metrics-container")
            ], className="section"),
            
            # Charts Row 1: Growth and Country Distribution
            html.Div([
                html.Div([
                    html.H4("📈 Netflix Content Growth"),
                    dcc.Graph(id="netflix-growth-chart")
                ], className="chart-container", style={'width': '50%'}),
                
                html.Div([
                    html.H4("🌍 Top Countries by Platform"),
                    dcc.Graph(id="countries-chart")
                ], className="chart-container", style={'width': '50%'})
            ], className="charts-row"),
            
            # Charts Row 2: Genre Analysis
            html.Div([
                html.Div([
                    html.H4("🎭 Genre Popularity"),
                    dcc.Graph(id="genre-popularity-chart")
                ], className="chart-container", style={'width': '50%'}),
                
                html.Div([
                    html.H4("📊 Platform Ratings Distribution"),
                    dcc.Graph(id="platform-ratings-chart")
                ], className="chart-container", style={'width': '50%'})
            ], className="charts-row"),
            
            # Charts Row 3: Advanced Analysis
            html.Div([
                html.Div([
                    html.H4("🔄 Genre Distribution by Platform"),
                    dcc.Graph(id="genre-distribution-chart")
                ], className="chart-container", style={'width': '50%'}),
                
                html.Div([
                    html.H4("📅 Seasonal Release Patterns"),
                    dcc.Graph(id="seasonal-chart")
                ], className="chart-container", style={'width': '50%'})
            ], className="charts-row"),
            
            # Charts Row 4: Correlation Analysis
            html.Div([
                html.Div([
                    html.H4("⭐ Ratings vs Viewership"),
                    dcc.Graph(id="correlation-chart")
                ], className="chart-container", style={'width': '100%'})
            ], className="charts-row")
        ], className="dashboard-content")
    ], className="main-container")
])

if __name__ == '__main__':
    app.run_server(debug=True)
