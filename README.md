# Product Experimentation & Funnel Analytics

End-to-end product analytics case study using SQL, dbt, Python and Looker Studio to model a customer conversion funnel, evaluate an A/B product experiment and translate analytical findings into product recommendations.

## Project Overview

This project analyzes a simulated customer journey for a consumer fintech product.

The analysis evaluates whether a personalized product recommendation experience improves customer activation and application conversion compared with the existing experience.

The project combines customer, acquisition and application data into an analytics-ready dbt model and evaluates product performance across experiment variants, platforms and acquisition channels.

## Business Questions

The analysis focuses on five questions:

1. Where are users dropping out of the product funnel?
2. Does the treatment experience improve customer activation?
3. Does treatment improve application completion?
4. Is the observed conversion lift statistically significant?
5. Does experiment performance differ across acquisition channels or platforms?

## Tech Stack

- SQL
- dbt
- Python
- pandas
- NumPy
- statsmodels
- DuckDB
- matplotlib
- Looker Studio
- Git / GitHub

## Data

The project uses simulated customer-level data representing 20,000 users.

Three core datasets are modeled:

### Customers

Contains:

- Customer ID
- Signup date
- Experiment assignment

### Acquisition

Contains:

- Acquisition touchpoints
- Paid social
- Search
- Referral
- Mobile
- Web

Multiple acquisition touchpoints are included for a subset of customers so first-touch acquisition can be identified using SQL window functions.

### Applications

Contains product-funnel activity:

- Recommendation shown
- Recommendation clicked
- Activated
- Application started
- Application completed

No real customer or confidential financial data is used.

## Analytics Engineering

Raw datasets are loaded as dbt seeds and transformed through staging and reporting models.

The SQL modeling workflow demonstrates:

- Joins
- Aggregates
- Subqueries
- CTEs
- Window functions
- Data validation
- dbt tests
- Reusable analytics models

The primary analysis-ready table is:

`fct_product_funnel`

It combines customer, acquisition and application information into one customer-level product analytics model.

## Product Funnel

The funnel analyzed is:

Signup  
↓  
Recommendation Click  
↓  
Activation  
↓  
Application Start  
↓  
Application Completion

Key KPIs include:

- Recommendation click-through rate
- Activation rate
- Application-start rate
- Application-completion rate
- Funnel drop-off
- Conversion lift

## A/B Experiment

Customers are randomly assigned to:

- Control — standard product recommendation experience
- Treatment — personalized recommendation experience

Python is used to calculate:

- Control conversion
- Treatment conversion
- Absolute conversion lift
- Relative conversion lift
- Two-proportion z-test
- P-value
- 95% confidence interval

A result is considered statistically significant when:

`p < 0.05`

## Segment Analysis

Experiment results are evaluated across:

### Platform

- Mobile
- Web

### Acquisition Channel

- Paid Social
- Search
- Referral

This helps determine whether the treatment effect is consistent across customer acquisition sources.

## Product Recommendation

The analysis translates experiment results into a rollout recommendation for a Product Manager.

The recommendation considers:

- Overall conversion lift
- Statistical significance
- Confidence intervals
- Platform-level performance
- Acquisition-channel performance

The final recommendation is generated in:

`docs/product_recommendation.md`

## Looker Studio

Python exports three analysis-ready reporting files:

- `looker_experiment_summary.csv`
- `looker_segment_results.csv`
- `looker_funnel_summary.csv`

These files support a Looker Studio dashboard containing:

- Product KPI cards
- Conversion funnel
- Control vs treatment performance
- Segment analysis
- Experiment decision metrics

## Repository Structure

```text
product-experimentation-funnel-analytics/
│
├── data/
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── seeds/
│
├── notebooks/
├── sql/
├── dashboard/
├── docs/
│
├── README.md
└── requirements.txt
