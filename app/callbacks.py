# Dashboard callbacks
from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def register_callbacks(app, df, countries_df, platforms):
    
    @app.callback(
        Output('key-metrics', 'children'),
        [Input('platform-selector', 'value'),
         Input('year-slider', 'value'),
         Input('rating-slider', 'value')]
    )
    def update_metrics(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return [
                html.Div([
                    html.Div("--", style={
                        'fontSize': '28px', 
                        'fontWeight': '700', 
                        'color': '#6c757d',
                        'fontFamily': 'Montserrat, sans-serif',
                        'lineHeight': '1.2'
                    }),
                    html.Div("Select Platforms", style={
                        'fontSize': '12px', 
                        'color': '#6c757d', 
                        'marginTop': 6,
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '500',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    })
                ], style={
                    'textAlign': 'center', 
                    'padding': '20px 16px', 
                    'backgroundColor': '#f8f9fa',
                    'border': 'none',
                    'borderLeft': '4px solid #6c757d',
                    'borderRadius': '12px',
                    'marginBottom': 12,
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
                    'transition': 'all 0.3s ease'
                }) for _ in range(3)
            ]
        
        filtered_df = filter_data(df, selected_platforms, year_range, rating_range)
        
        total_titles = len(filtered_df)
        avg_rating = filtered_df['vote_average'].mean() if len(filtered_df) > 0 else 0
        total_countries = len(set([country for countries in filtered_df['country_names'] 
                                 for country in countries if countries and len(filtered_df) > 0]))
        
        metrics = [
            {'label': 'Total Titles', 'value': f"{total_titles:,}", 'color': '#3498db'},
            {'label': 'Avg Rating', 'value': f"{avg_rating:.1f}/10", 'color': '#e74c3c'},
            {'label': 'Countries', 'value': f"{total_countries}", 'color': '#2ecc71'}
        ]
        
        return [
            html.Div([
                html.Div(metric['value'], style={
                    'fontSize': '28px', 
                    'fontWeight': '700', 
                    'color': metric['color'],
                    'fontFamily': 'Montserrat, sans-serif',
                    'lineHeight': '1.2'
                }),
                html.Div(metric['label'], style={
                    'fontSize': '12px', 
                    'color': '#6c757d', 
                    'marginTop': 6,
                    'fontFamily': 'Montserrat, sans-serif',
                    'fontWeight': '500',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                })
            ], style={
                'textAlign': 'center', 
                'padding': '20px 16px', 
                'backgroundColor': '#ffffff',
                'border': 'none',
                'borderLeft': f'4px solid {metric["color"]}',
                'borderRadius': '12px',
                'marginBottom': 12,
                'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
                'transition': 'all 0.3s ease'
            }) for metric in metrics
        ]
    
    @app.callback(
        Output('netflix-growth-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_netflix_growth(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_df = df[
            (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
            (df['vote_average'] >= rating_range[0]) & (df['vote_average'] <= rating_range[1])
        ]
        
        # Modern platform colors with better contrast
        platform_colors = {
            'Netflix': '#E50914',
            'Hulu': '#1CE783', 
            'Prime Video': '#00A8E1',
            'Disney+': '#113CCF'
        }
        
        fig = go.Figure()
        
        # Create smooth area charts for each platform
        for i, platform in enumerate(selected_platforms):
            if platform in filtered_df.columns:
                platform_growth = filtered_df[filtered_df[platform] == 1].groupby('Year').size().reset_index(name='count')
                
                # Add smooth area trace
                fig.add_trace(go.Scatter(
                    x=platform_growth['Year'],
                    y=platform_growth['count'],
                    mode='lines',
                    name=platform,
                    line=dict(
                        color=platform_colors.get(platform, '#3498db'), 
                        width=3,
                        shape='spline',
                        smoothing=0.3
                    ),
                    fill='tonexty' if i > 0 else 'tozeroy',
                    fillcolor=f"rgba{tuple(list(bytes.fromhex(platform_colors.get(platform, '#3498db')[1:])) + [0.2])}",
                    hovertemplate=f'<b>{platform}</b><br>' +
                                 'Year: %{x}<br>' +
                                 'Titles: %{y}<br>' +
                                 '<extra></extra>'
                ))
        
        fig.update_layout(
            xaxis_title="Release Year",
            yaxis_title="Number of Titles",
            font=dict(size=13, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12, family='Montserrat, sans-serif')
            ),
            margin=dict(t=60, l=60, r=40, b=60),
            hovermode='x unified'
        )
        
        # Clean grid styling
        fig.update_xaxes(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1,
            showline=True,
            linecolor='rgba(0,0,0,0.1)',
            linewidth=1
        )
        fig.update_yaxes(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1,
            showline=True,
            linecolor='rgba(0,0,0,0.1)',
            linewidth=1
        )
        
        return fig
    
    @app.callback(
        Output('world-map-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_world_map(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_countries_df = filter_countries_data(countries_df, selected_platforms, year_range, rating_range)
        
        if len(filtered_countries_df) == 0:
            return go.Figure().add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        country_counts = filtered_countries_df['country'].value_counts().reset_index()
        country_counts.columns = ['country', 'content_count']
        
        fig = px.choropleth(
            country_counts,
            locations='country',
            color='content_count',
            locationmode='country names',
            color_continuous_scale='Viridis',
            title='',
            labels={'content_count': 'Content Count'}
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            font=dict(size=12, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @app.callback(
        Output('genre-heatmap-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_genre_heatmap(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_df = filter_data(df, selected_platforms, year_range, rating_range)
        
        # Create platform-genre matrix
        platform_genre_data = []
        for platform in selected_platforms:
            platform_data = filtered_df[filtered_df[platform] == 1]
            if len(platform_data) > 0:
                genre_counts = platform_data['genres'].value_counts().head(10)
                for genre, count in genre_counts.items():
                    platform_genre_data.append({
                        'Platform': platform,
                        'Genre': genre,
                        'Content Count': count
                    })
        
        if not platform_genre_data:
            return go.Figure().add_annotation(
                text="No genre data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        heatmap_df = pd.DataFrame(platform_genre_data)
        heatmap_pivot = heatmap_df.pivot(index='Genre', columns='Platform', values='Content Count').fillna(0)
        
        fig = px.imshow(
            heatmap_pivot,
            title='',
            color_continuous_scale='Blues',
            aspect='auto'
        )
        
        fig.update_layout(
            xaxis_title="Streaming Platform",
            yaxis_title="Content Genre",
            font=dict(size=12, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @app.callback(
        Output('platform-comparison-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_platform_comparison(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_df = filter_data(df, selected_platforms, year_range, rating_range)
        
        platform_stats = []
        for platform in selected_platforms:
            platform_data = filtered_df[filtered_df[platform] == 1]
            if len(platform_data) > 0:
                platform_stats.append({
                    'Platform': platform,
                    'Average Rating': platform_data['vote_average'].mean(),
                    'Total Content': len(platform_data),
                    'Total Votes': platform_data['vote_count'].sum()
                })
        
        if not platform_stats:
            return go.Figure().add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        stats_df = pd.DataFrame(platform_stats)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Rating', 'Total Content', 'Total Engagement', 'Rating Distribution'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "violin"}]]
        )
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        # Average Rating
        fig.add_trace(
            go.Bar(x=stats_df['Platform'], y=stats_df['Average Rating'], 
                   marker_color=colors[0], showlegend=False),
            row=1, col=1
        )
        
        # Total Content
        fig.add_trace(
            go.Bar(x=stats_df['Platform'], y=stats_df['Total Content'],
                   marker_color=colors[1], showlegend=False),
            row=1, col=2
        )
        
        # Total Votes
        fig.add_trace(
            go.Bar(x=stats_df['Platform'], y=stats_df['Total Votes'],
                   marker_color=colors[2], showlegend=False),
            row=2, col=1
        )
        
        # Rating Distribution
        for i, platform in enumerate(selected_platforms):
            platform_data = filtered_df[filtered_df[platform] == 1]['vote_average'].dropna()
            if len(platform_data) > 0:
                fig.add_trace(
                    go.Violin(y=platform_data, name=platform, 
                             line_color=colors[i % len(colors)], showlegend=False),
                    row=2, col=2
                )
        
        fig.update_layout(height=500, font=dict(size=10, family='Montserrat, sans-serif'))
        return fig
    
    @app.callback(
        Output('countries-bar-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_countries_bar(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_countries_df = filter_countries_data(countries_df, selected_platforms, year_range, rating_range)
        
        # Handle empty filtered data
        if len(filtered_countries_df) == 0:
            return go.Figure().add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        # Get top countries across all selected platforms
        country_counts = filtered_countries_df['country'].value_counts().head(15)
        
        # Handle case where country_counts is empty
        if len(country_counts) == 0:
            return go.Figure().add_annotation(
                text="No country data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        fig = px.bar(
            x=country_counts.values,
            y=country_counts.index,
            orientation='h',
            title='',
            color=country_counts.values,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            xaxis_title="Number of Titles",
            yaxis_title="Country",
            font=dict(size=12, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
    
    @app.callback(
        Output('seasonal-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_seasonal_chart(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_df = filter_data(df, selected_platforms, year_range, rating_range)
        
        # Create monthly release patterns data
        monthly_data = []
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for platform in selected_platforms:
            platform_data = filtered_df[filtered_df[platform] == 1]
            if 'release_month' in platform_data.columns and len(platform_data) > 0:
                monthly_counts = platform_data.groupby('release_month').size()
                for month in range(1, 13):
                    count = monthly_counts.get(month, 0)
                    monthly_data.append({
                        'Platform': platform,
                        'Month': month_names[month-1],
                        'Count': count
                    })
        
        if not monthly_data:
            return go.Figure().add_annotation(
                text="No seasonal data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        monthly_df = pd.DataFrame(monthly_data)
        
        fig = px.line(monthly_df, x='Month', y='Count', color='Platform',
                     title='', markers=True)
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Releases",
            font=dict(size=12, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
    
    @app.callback(
        Output('correlation-chart', 'figure'),
        [Input('platform-selector', 'value'), Input('year-slider', 'value'), Input('rating-slider', 'value')]
    )
    def update_correlation_chart(selected_platforms, year_range, rating_range):
        # Handle empty platform selection
        if not selected_platforms:
            return go.Figure().add_annotation(
                text="Please select at least one streaming platform",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        filtered_df = filter_data(df, selected_platforms, year_range, rating_range)
        
        # Create scatter plot of ratings vs vote count
        correlation_data = filtered_df[['vote_average', 'vote_count']].dropna()
        
        if len(correlation_data) == 0:
            return go.Figure().add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=16, color="#6c757d", family='Montserrat, sans-serif'),
                showarrow=False
            )
        
        correlation = correlation_data.corr().iloc[0, 1]
        
        fig = px.scatter(
            correlation_data, 
            x='vote_average', 
            y='vote_count',
            title='',
            opacity=0.6,
            color_discrete_sequence=['#3498db']
        )
        
        fig.update_layout(
            xaxis_title="Average Rating",
            yaxis_title="Total Votes",
            font=dict(size=12, family='Montserrat, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    x=0.05,
                    y=0.95,
                    xref="paper",
                    yref="paper",
                    text=f"Correlation: {correlation:.3f}",
                    showarrow=False,
                    font=dict(size=14, color='#2c3e50', family='Montserrat, sans-serif'),
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='#bdc3c7',
                    borderwidth=1
                )
            ]
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        return fig

def filter_data(df, selected_platforms, year_range, rating_range):
    if not selected_platforms:
        return pd.DataFrame()  # Return empty DataFrame if no platforms selected
    
    platform_filter = df[selected_platforms].sum(axis=1) > 0
    filtered_df = df[
        platform_filter &
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
        (df['vote_average'] >= rating_range[0]) & (df['vote_average'] <= rating_range[1])
    ]
    return filtered_df

def filter_countries_data(countries_df, selected_platforms, year_range, rating_range):
    if not selected_platforms:
        return pd.DataFrame()  # Return empty DataFrame if no platforms selected
        
    platform_filter = countries_df[selected_platforms].sum(axis=1) > 0
    filtered_df = countries_df[
        platform_filter &
        (countries_df['Year'] >= year_range[0]) & (countries_df['Year'] <= year_range[1]) &
        (countries_df['vote_average'] >= rating_range[0]) & (countries_df['vote_average'] <= rating_range[1])
    ]
    return filtered_df
