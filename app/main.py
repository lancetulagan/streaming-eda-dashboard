# Streaming Platforms Dashboard
import dash
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap'
])
app.title = "Streaming Platforms Dashboard"

def load_data():
    """Load and prepare the data"""
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'datasets', 'cleaned', 'movies_cleaned.csv')
    df = pd.read_csv(data_path)
    
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
    
    df['country_names'] = df['production_countries'].apply(extract_country_names)
    df['language_names'] = df['spoken_languages'].apply(extract_language_names)
    
    countries_expanded = []
    for idx, row in df.iterrows():
        for country in row['country_names']:
            new_row = row.copy()
            new_row['country'] = country
            countries_expanded.append(new_row)
    
    countries_df = pd.DataFrame(countries_expanded)
    
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_month'] = df['release_date'].dt.month
    df['release_year'] = df['release_date'].dt.year
    
    return df, countries_df

df, countries_df = load_data()
platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']

# Get reasonable year range (streaming era)
min_year = max(2000, df['Year'].min())  # Start from 2000 or data minimum
max_year = df['Year'].max()

app.layout = html.Div([
    # Fixed Sticky Header
    html.Div([
        html.H1("Streaming Platforms Content Analysis", style={
            'margin': 0, 
            'color': '#ffffff',  # Changed to white
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '700',
            'fontSize': '28px',
            'letterSpacing': '-0.5px'
        }),
        html.P("Interactive Dashboard for Content Strategy & Market Analysis", style={
            'margin': '8px 0 0 0', 
            'color': '#ffffff',  # Changed to white
            'fontSize': '16px',
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '400',
            'opacity': '0.9'  # Slightly transparent for subtle effect
        })
    ], style={
        'textAlign': 'center', 
        'padding': '24px 0', 
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'color': 'white',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'right': 0,
        'zIndex': 1001,
        'boxShadow': '0 4px 12px rgba(0,0,0,0.15)'
    }),
    
    html.Div([
        # Fixed Sidebar Controls
        html.Div([
            html.H3("Dashboard Controls", style={
                'color': '#1a1a1a', 
                'marginTop': 0,
                'fontFamily': 'Montserrat, sans-serif',
                'fontWeight': '600',
                'fontSize': '20px',
                'marginBottom': '24px'
            }),
            
            html.Div([
                html.Label("Streaming Platforms:", style={
                    'fontWeight': '500', 
                    'marginBottom': 12, 
                    'display': 'block',
                    'fontFamily': 'Montserrat, sans-serif',
                    'color': '#495057',
                    'fontSize': '14px'
                }),
                dcc.Checklist(
                    id='platform-selector',
                    options=[{'label': platform, 'value': platform} for platform in platforms],
                    value=platforms,
                    style={'marginBottom': 28},
                    labelStyle={
                        'display': 'block', 
                        'marginBottom': 10,
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontSize': '13px',
                        'color': '#6c757d'
                    }
                )
            ]),
            
            html.Div([
                html.Label("Release Year Range:", style={
                    'fontWeight': '500', 
                    'marginBottom': 12, 
                    'display': 'block',
                    'fontFamily': 'Montserrat, sans-serif',
                    'color': '#495057',
                    'fontSize': '14px'
                }),
                dcc.RangeSlider(
                    id='year-slider',
                    min=min_year,
                    max=max_year,
                    value=[min_year, max_year],
                    step=1,
                    marks={year: {'label': f'{year}', 'style': {'fontSize': 10, 'fontFamily': 'Montserrat'}} 
                           for year in range(min_year, max_year + 1, 5)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'marginBottom': 28}),
            
            html.Div([
                html.Label("Content Rating Range:", style={
                    'fontWeight': '500', 
                    'marginBottom': 12, 
                    'display': 'block',
                    'fontFamily': 'Montserrat, sans-serif',
                    'color': '#495057',
                    'fontSize': '14px'
                }),
                dcc.RangeSlider(
                    id='rating-slider',
                    min=0,
                    max=10,
                    value=[0, 10],
                    step=0.5,
                    marks={i: {'label': f'{i}', 'style': {'fontSize': 10, 'fontFamily': 'Montserrat'}} 
                           for i in range(0, 11, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'marginBottom': 28}),
            
            # Key Metrics Summary
            html.Div([
                html.H4("Key Metrics", style={
                    'color': '#1a1a1a', 
                    'marginBottom': 16,
                    'fontFamily': 'Montserrat, sans-serif',
                    'fontWeight': '600',
                    'fontSize': '16px'
                }),
                html.Div(id="key-metrics", style={'maxHeight': '250px', 'overflowY': 'auto'})
            ])
            
        ], style={
            'position': 'fixed',
            'left': 0,
            'top': 110,  # Account for sticky header height
            'width': 300,
            'height': 'calc(100vh - 110px)',
            'background': 'linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%)',
            'padding': '24px',
            'borderRight': '1px solid #e9ecef',
            'overflowY': 'auto',
            'zIndex': 1000,
            'boxShadow': '4px 0 12px rgba(0,0,0,0.05)'
        }),
        
        # Main Content Area
        html.Div([
            # Netflix Growth & Global Distribution Row
            html.Div([
                html.Div([
                    html.H4("Platform Content Library Growth", style={
                        'color': '#1a1a1a', 
                        'marginBottom': 20,
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '600',
                        'fontSize': '18px'
                    }),
                    dcc.Graph(id="netflix-growth-chart", style={'height': 450})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                html.Div([
                    html.H4("Global Content Production Distribution", style={
                        'color': '#1a1a1a', 
                        'marginBottom': 20,
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '600',
                        'fontSize': '18px'
                    }),
                    dcc.Graph(id="world-map-chart", style={'height': 450})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
            ], style={'marginBottom': 40}),
            
            # Genre Analysis Row
            html.Div([
                html.Div([
                    html.H4("Genre Popularity Heatmap by Platform", style={'color': '#2c3e50', 'marginBottom': 15}),
                    dcc.Graph(id="genre-heatmap-chart", style={'height': 500})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                html.Div([
                    html.H4("Platform Performance Comparison", style={'color': '#2c3e50', 'marginBottom': 15}),
                    dcc.Graph(id="platform-comparison-chart", style={'height': 500})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
            ], style={'marginBottom': 30}),
            
            # Time Series & Correlation Row
            html.Div([
                html.Div([
                    html.H4("Seasonal Content Release Patterns", style={'color': '#2c3e50', 'marginBottom': 15}),
                    dcc.Graph(id="seasonal-chart", style={'height': 400})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                html.Div([
                    html.H4("Content Ratings vs Viewership Analysis", style={'color': '#2c3e50', 'marginBottom': 15}),
                    dcc.Graph(id="correlation-chart", style={'height': 400})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
            ], style={'marginBottom': 30}),
            
            # Full Width Regional Analysis
            html.Div([
                html.H4("Top Content Producing Countries by Platform", style={'color': '#2c3e50', 'marginBottom': 15}),
                dcc.Graph(id="countries-bar-chart", style={'height': 600})
            ], style={'marginBottom': 30})
            
        ], style={
            'marginLeft': 340,  # Account for wider sidebar
            'marginTop': 130,   # Account for sticky header
            'padding': '24px',
            'backgroundColor': '#ffffff',
            'minHeight': 'calc(100vh - 130px)',
            'fontFamily': 'Montserrat, sans-serif'
        })
    ])
])

# Register callbacks
register_callbacks(app, df, countries_df, platforms)

if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
