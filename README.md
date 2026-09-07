# Product Experimentation & Funnel Analytics

End-to-end product analytics project using **SQL, dbt, Python, and Looker Studio** to model customer funnel data, evaluate an A/B experiment, and translate analytical findings into product recommendations.

## Project Overview

This project analyzes a simulated digital product funnel for a consumer fintech platform. The goal is to understand how users move from acquisition through application completion and evaluate whether a personalized product experience improves conversion.

The analysis combines customer, acquisition, application, and experiment data to support product and marketing decisions.

## Business Questions

* Where are the largest drop-offs in the customer funnel?
* Does the treatment experience improve activation or conversion?
* Is the observed conversion lift statistically significant?
* Which customer or acquisition segments respond best to the treatment?
* Should the new experience be rolled out more broadly?

## Tools & Technologies

* **SQL**
* **dbt**
* **Python**
* **pandas**
* **NumPy**
* **statsmodels**
* **Looker Studio**
* **Git / GitHub**

## Analysis Workflow

1. Prepare and validate raw customer, acquisition, application, and experiment datasets
2. Create staging, intermediate, and reporting models using dbt
3. Use SQL joins, aggregates, subqueries, CTEs, and window functions to build analysis-ready tables
4. Calculate funnel and performance KPIs
5. Evaluate treatment and control groups using statistical testing
6. Analyze experiment performance by customer and acquisition segment
7. Summarize findings in a product decision recommendation
8. Present key metrics and trends through a Looker Studio dashboard

## Key Metrics

The project evaluates metrics including:

* Activation rate
* Recommendation click-through rate
* Application-start rate
* Application-completion rate
* Funnel drop-off
* Conversion lift
* Confidence intervals
* Statistical significance
* Performance by mobile and web users
* Paid social, search, and referral conversion

## Repository Structure

```text
product-experimentation-funnel-analytics/
│
├── README.md
├── data/
├── sql/
├── dbt/
├── notebooks/
├── dashboard/
└── docs/
```

## Project Status

Project developed in 2026 as a portfolio case study in product analytics, experimentation, data modeling, and business decision support.
