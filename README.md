# Streaming Platforms Data Analysis

A data visualization project exploring streaming platform content trends and patterns.

## About

I created this project for my Data Visualization course at DLSU to analyze how different streaming platforms (Netflix, Hulu, Prime Video, Disney+) compare in terms of content diversity, ratings, and release patterns. The project includes both an exploratory data analysis notebook and an interactive dashboard.

## What's Inside

- **EDA Notebook** (`notebooks/eda.ipynb`) - My analysis covering 8 research questions about streaming content
- **Interactive Dashboard** (`app/`) - A Plotly Dash web app with filters and visualizations
- **Dataset** (`datasets/`) - Movie/TV show data with streaming platform availability

## Key Findings

Through my analysis, I discovered some interesting patterns:
- Genre preferences vary significantly between platforms
- Seasonal release patterns show clear trends
- Rating distributions differ across streaming services
- Content production has shifted dramatically over the decades

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Dashboard
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

The dashboard will open at `http://localhost:8053`

### Exploring the Data
Open `notebooks/eda.ipynb` in Jupyter to see my full analysis process.

## Project Structure
```
├── README.md
├── requirements.txt
├── run_dashboard.sh
├── app/
│   ├── main.py          # Dashboard layout
│   ├── callbacks.py     # Interactive functions
│   └── assets/
│       └── style.css    # Custom styling
├── datasets/
│   ├── raw/             # Original data files
│   └── cleaned/         # Processed data
└── notebooks/
    ├── data_cleaning.ipynb
    └── eda.ipynb        # Main analysis
```

## Tech Stack

- **Python** - pandas, plotly, dash
- **Visualization** - Plotly Express, Seaborn
- **Dashboard** - Dash with custom CSS
- **Data Processing** - JSON parsing for country/language data

## Course Context

This project was completed for DATANVI - Data Visualization at De La Salle University. It demonstrates data cleaning, exploratory analysis, and interactive visualization techniques applied to real-world streaming platform data.

---

