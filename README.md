# Automated Sales Reporting System

An automated Python-based reporting system that loads e-commerce transaction data, cleans and analyses the data, retrieves public holiday information, generates visual reports and Excel reports, and delivers the reports by email.

## Project Features

- CSV data loading
- Data cleaning
- Duplicate removal
- Missing value handling
- Country name standardisation
- Revenue calculation
- Public holiday API integration
- Country-specific holiday matching
- Weekly sales analysis
- Automated charts
- Excel report generation
- Email delivery
- Automation logging

## Project Structure

```text
Month1_automated_reporter/
│
├── data/
│   ├── ecommerce_retail_transactions_raw.csv
│   └── README.md
│
├── output/
│   ├── reports/
│   └── charts/
│
├── logs/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── analyzer.py
│   ├── visualizer.py
│   ├── report_generator.py
│   └── email_sender.py
│
├── main.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore