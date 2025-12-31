# S&P 500 Performance Dashboard

Interactive analytics platform for exploring revenue growth and profitability relationships across S&P 500 companies.

![Dashboard Overview](images/scatterplot.png)

## Problem

Investment analysts need to rapidly test hypotheses across financial and geographic dimensions. This dashboard enables dynamic filtering and visualization of 500+ companies, reducing analysis time from minutes to seconds.

**Example Query**: "Show technology and healthcare companies with specific employee counts and market cap ranges"

## Features

**Multi-dimensional Filtering**
- Sector selection (11 categories)
- Market cap range slider
- Employee count range slider
- Real-time filtering with instant visualization updates

**Interactive Visualizations**

Revenue Growth vs EBITDA scatter plot with hover details and sector coloring:

![Scatter Plot](images/scatterplot.png)

Sector performance comparison showing average revenue growth:

![Sector Analysis](images/sectoranalysis.png)

Top performers ranking table with sortable columns:

![Top Performers](images/topperformers.png)

## Technical Implementation

**Architecture**
```
sp500_api.py          # Data layer: loading, filtering, aggregation
sp500_dashboard.py    # UI layer: widgets, visualizations, callbacks
```

**Data Processing**
- Dataset: 502 companies, 16 attributes
- Preprocessing: removes incomplete records, normalizes to readable units
- Performance: vectorized pandas filtering, sub-100ms response times

**Tech Stack**: Python, Pandas, Plotly, Holoviz Panel

## Installation
```bash
git clone https://github.com/YOUR-USERNAME/sp500-dashboard.git
cd sp500-dashboard
pip install -r requirements.txt
python sp500_dashboard.py
```

Dashboard opens at `localhost:5006`

## Project Structure
```
sp500-dashboard/
├── sp500_api.py
├── sp500_dashboard.py
├── requirements.txt
├── data/
│   └── sp500_companies.csv
└── images/
    ├── scatterplot.png
    ├── sectoranalysis.png
    └── topperformers.png
```

## Use Cases

Investment screening, sector analysis, employee size analysis, market cap filtering, outlier detection

## Technical Highlights

- Clean API design pattern with separation of concerns
- Efficient vectorized pandas operations
- Callback-based UI updates for instant filtering
- Production-ready modular code structure

## Author

Nikhil

Built to demonstrate proficiency in data visualization, API design, and financial analytics.