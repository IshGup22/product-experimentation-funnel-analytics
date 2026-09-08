# Looker Studio Dashboard

The reporting outputs in this folder are designed to be connected to Google Looker Studio for product and experiment reporting.

## Data Sources

### looker_experiment_summary.csv

Contains overall control and treatment results for:

- Recommendation click-through rate
- Activation rate
- Application-start rate
- Application-completion rate
- Absolute conversion lift
- Relative conversion lift
- 95% confidence intervals
- Statistical significance

### looker_segment_results.csv

Contains experiment performance segmented by:

- Mobile
- Web
- Paid social
- Search
- Referral

### looker_funnel_summary.csv

Contains customer counts and conversion rates across:

1. Signup
2. Recommendation click
3. Activation
4. Application start
5. Application completion

## Recommended Dashboard Layout

### KPI Cards

- Treatment conversion rate
- Control conversion rate
- Conversion lift
- Activation rate
- Experiment p-value

### Funnel Visualization

Display users across each stage:

Signup → Recommendation Click → Activation → Application Start → Application Completion

### Segment Performance

Compare treatment and control conversion across:

- Mobile vs Web
- Paid Social
- Search
- Referral

### Experiment Decision

Include the experiment recommendation and whether the observed conversion improvement is statistically significant.
