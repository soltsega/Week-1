Predicting Price Moves with News Sentiment (Week 1 Challenge)

🎯 Challenge Overview

This project, part of the 10 Academy AI Mastery program, focuses on correlating the sentiment extracted from financial news headlines with real-world stock market movements. This is a crucial exercise in combining Data Engineering (DE), Financial Analytics (FA), and Natural Language Processing (NLP) techniques to enhance predictive models.

Business Objective: To provide Nova Financial Solutions with actionable investment strategies by demonstrating a statistically significant correlation between news sentiment scores and corresponding daily stock returns.

⭐ Project Significance & Financial Impact

This project is directly aligned with Nova Financial Solutions' goal to boost financial forecasting accuracy. By establishing a quantifiable link between news sentiment and stock returns, the analysis aims to:

Develop a Novel Predictive Feature: Sentiment scores extracted from headlines serve as a new, forward-looking data point that can be incorporated into larger quantitative trading models.

Enhance Trading Strategy: The derived correlations will suggest innovative investment strategies (e.g., "Buy on highly positive sentiment news release if technical indicators confirm upward momentum").

Measure Market Efficiency: Analyzing the time delay between news publication, sentiment aggregation, and price reaction helps to gauge the efficiency of the market for specific stocks or sectors.

🛠️ Skills Demonstrated (KPIs)

This challenge demands the demonstration of core skills across the data science and financial engineering pipeline:

Skill Area

Key Performance Indicators (KPIs) Demonstrated

Data Engineering

Configuring a reproducible Python environment (requirements.txt), implementing robust Git version control, and modularizing code into src/ and scripts/.

Data & Time Series Analysis

Performing detailed EDA on text and time-series data, including temporal distribution analysis and data alignment across different sources.

Financial Analytics

Sourcing and preparing historical OHLCV data, accurately calculating daily stock returns, and computing standard technical indicators (MA, RSI, MACD) using TA-Lib.

Natural Language Processing (NLP)

Applying appropriate NLP tools (e.g., TextBlob/VADER) for financial sentiment analysis and aggregating results for correlation testing.

Statistical Analysis & Reporting

Measuring the Pearson correlation coefficient to quantify the strength of the relationship, and documenting findings in a concise, publication-style report.

💾 Dataset and Data Sourcing

The analysis utilizes a combination of two primary data sources:

Financial News and Stock Price Integration Dataset (FNSPID): The core dataset containing financial news articles, including:

headline: The text subject to sentiment analysis.

date: The publication date and time (UTC-4), which requires normalization.

stock: The associated ticker symbol.

publisher: The source of the news article.

External Stock Price Data: Historical OHLCV (Open, High, Low, Close, Volume) data for all unique stock tickers are acquired from a reliable financial data API (e.g., Yahoo Finance via yfinance or pynance) to calculate daily returns and technical indicators.

🏗️ Project Structure

The repository follows the modular structure specified in the challenge document for clear separation of concerns:

├── .vscode/
├── .github/
│   └── workflows
│       └── unittests.yml  # CI/CD Workflow (Future)
├── .gitignore
├── requirements.txt       # Project dependencies
├── README.md              # This file
├── src/                   # Source code for reusable functions (data cleaning, indicators, sentiment)
│   ├── __init__.py
│   └── processing.py
├── notebooks/             # Exploratory Data Analysis and primary analysis scripts
│   ├── __init__.py
│   ├── 1.0_EDA.ipynb      # Task 1 EDA (Text, Time Series, Publisher)
│   └── 2.0_Quantitative_Analysis.ipynb # Task 2 & 3 (Indicators, Sentiment, Correlation)
├── tests/                 # Unit tests for functions in src/ (Future)
└── scripts/               # Utility scripts (e.g., data downloading, environment setup)



🛠️ Setup and Installation

Prerequisites

Python 3.8+

Git

TA-Lib installation (requires pre-installation before pip install TA-Lib)

Installation

Clone the Repository:

git clone [https://github.com/soltsega/Week-1.git](https://github.com/soltsega/Week-1.git)
cd Week-1



Create and Activate Environment:
It is highly recommended to use a virtual environment (e.g., venv or conda):

python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows



Install Dependencies:
The project relies on standard data science and finance libraries.

pip install -r requirements.txt



Note: This file includes pandas, numpy, matplotlib, seaborn, yfinance (or similar), and NLP packages like nltk and TextBlob.

📈 Tasks and Methodology

Task 1: Git and GitHub / Exploratory Data Analysis (Completed)

Goal: Establish version control and gain initial insights from the news dataset.

Methodology: Analysis covered headline length distribution, publisher frequency, temporal trends in news volume, and keyword extraction.

Artifact: notebooks/1.0_EDA.ipynb

Task 2: Quantitative Analysis using pynance and TaLib (In Progress)

Goal: Acquire historical stock data, align it with news articles, and calculate market indicators.

Methodology:

Use yfinance/pynance to download OHLCV data for all unique tickers.

Normalize news timestamps (UTC-4) to align precisely with the daily closing price of the corresponding trading day.

Employ TA-Lib (via its Python wrapper) to calculate key technical indicators, including:

Moving Averages (SMA, EMA): Used for trend following.

Relative Strength Index (RSI): Used for measuring momentum and overbought/oversold levels.

MACD (Moving Average Convergence Divergence): Used for signaling momentum shifts.

Task 3: Correlation between News and Stock Movement (Planned)

Goal: Quantify the link between news tone and market reaction, resulting in actionable insights.

Methodology:

Sentiment Analysis: Apply an NLP tool (e.g., TextBlob/VADER) to the headline column to generate a continuous sentiment score (polarity/subjectivity).

Daily Returns: Compute the daily percentage change in stock closing prices, representing stock movement.

Aggregation: Aggregate sentiment scores (e.g., compute the average or weighted average sentiment) by date and stock ticker, ensuring multiple news items on a single day result in a single daily sentiment metric.

Correlation: Calculate the Pearson Correlation Coefficient between the aggregated daily sentiment scores and the daily stock returns. This value (e.g., a correlation strength of +0.X) will be the primary technical deliverable.

🤝 Next Steps and Collaboration

Finalize data processing, alignment, and technical indicator calculation.

Execute Task 3: Sentiment Analysis and Correlation.

Draft the Final Report/Medium Blog Post, focusing on visualization and interpretation of the correlation findings.

Please raise any issues or suggest improvements via the GitHub issues tab: https://github.com/soltsega/Week-1/issues.
