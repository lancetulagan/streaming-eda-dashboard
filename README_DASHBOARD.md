# 🎬 Streaming Platforms Interactive Dashboard

An interactive dashboard built with Plotly Dash to analyze and visualize streaming platform content data from Netflix, Hulu, Prime Video, and Disney+.

## ✨ Features

### 📊 Interactive Controls
- **Platform Selector**: Choose which streaming platforms to analyze
- **Year Range Slider**: Filter content by release year
- **Rating Range Slider**: Filter content by user ratings

### 📈 Visualizations
1. **Key Metrics Cards**: Total titles, average rating, countries, and votes
2. **Netflix Growth Chart**: Content library growth over time
3. **Country Distribution**: Top content-producing countries by platform
4. **Genre Popularity**: Most popular genres by ratings and viewership
5. **Platform Ratings**: Rating distribution comparison across platforms
6. **Genre Distribution Heatmap**: Genre preferences by platform
7. **Seasonal Patterns**: Monthly content release trends
8. **Ratings vs Viewership**: Correlation analysis with scatter plot

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Running

1. **Clone or download the project**
2. **Navigate to the project directory**
3. **Run the dashboard:**

```bash
# Make the run script executable (macOS/Linux)
chmod +x run_dashboard.sh

# Run the dashboard
./run_dashboard.sh
```

**Or manually:**
```bash
# Install dependencies
pip install -r requirements.txt

# Navigate to app directory
cd app

# Run the dashboard
python main.py
```

4. **Open your browser and go to:** `http://127.0.0.1:8050`

## 📁 Project Structure

```
streaming-eda-dash/
├── app/
│   ├── main.py              # Main dashboard application
│   ├── callbacks.py         # Interactive callback functions
│   └── assets/
│       └── style.css        # Custom styling
├── datasets/
│   └── cleaned/
│       └── movies_cleaned.csv  # Processed data
├── notebooks/
│   └── eda.ipynb           # Exploratory data analysis
├── requirements.txt         # Python dependencies
├── run_dashboard.sh        # Quick start script
└── README.md               # This file
```

## 🎛️ Dashboard Controls

### Platform Selector
- Select one or multiple platforms to analyze
- Default: All platforms selected

### Year Range Slider
- Filter content by release year
- Dynamically updates all visualizations

### Rating Range Slider
- Filter content by user ratings (0-10)
- Helps focus on highly-rated or poorly-rated content

## 📊 Dashboard Sections

### 1. Key Metrics
Real-time metrics that update based on your filters:
- **Total Titles**: Number of titles matching your criteria
- **Average Rating**: Mean rating across selected content
- **Countries**: Number of unique production countries
- **Average Votes**: Mean vote count (viewership indicator)

### 2. Content Analysis Charts
- **Netflix Growth**: Shows how Netflix's library has expanded
- **Top Countries**: Horizontal bar charts showing content production by country
- **Genre Popularity**: Side-by-side comparison of ratings vs viewership by genre
- **Platform Ratings**: Box plots comparing rating distributions

### 3. Advanced Analysis
- **Genre Distribution**: Heatmap showing genre preferences by platform
- **Seasonal Patterns**: Line chart showing monthly release trends
- **Ratings vs Viewership**: Scatter plot with correlation analysis

## 🎨 Customization

### Styling
- Modify `app/assets/style.css` to customize the appearance
- Colors, fonts, and layout can be adjusted

### Adding New Features
- Add new callback functions in `callbacks.py`
- Update the layout in `main.py`
- Add corresponding HTML elements and graphs

## 📋 Data Requirements

The dashboard expects a CSV file with the following columns:
- Platform columns: `Netflix`, `Hulu`, `Prime Video`, `Disney+`
- `production_countries`: JSON string of country data
- `spoken_languages`: JSON string of language data
- `vote_average`: User ratings
- `vote_count`: Number of votes/views
- `genres`: Content genres
- `Year`: Release year
- `release_date`: Release date

## 🔧 Troubleshooting

### Common Issues

1. **Module not found errors**: Install requirements with `pip install -r requirements.txt`
2. **Data not loading**: Ensure `movies_cleaned.csv` is in the correct path
3. **Port already in use**: The dashboard runs on port 8050 by default

### Performance Tips
- For large datasets, consider implementing data sampling
- Use caching for expensive computations
- Optimize callback functions for better responsiveness

## 📈 Insights Answered

This dashboard helps answer key business questions:

1. **How has Netflix's content library grown over the years?**
2. **Which countries produce the most content on each platform?**
3. **What genre is the most popular in terms of viewership and ratings?**
4. **Which platform has the most highly rated content?**
5. **How does genre distribution differ across platforms?**
6. **Are certain platforms biased toward specific genres?**
7. **Are higher-rated movies also the most viewed?**
8. **Are there seasonal or regional trends in viewership for specific genres?**

## 🚀 Next Steps

Potential enhancements:
- Add more interactive filters (director, cast, etc.)
- Implement user authentication
- Add data export functionality
- Create mobile-responsive design
- Add real-time data updates
- Implement advanced analytics features

---

**Built with:** Python, Plotly Dash, Pandas, NumPy
**Author:** Data Visualization Project
**License:** MIT
