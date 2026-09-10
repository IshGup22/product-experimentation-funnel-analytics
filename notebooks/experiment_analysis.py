from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import norm
from statsmodels.stats.proportion import proportions_ztest


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    BASE_DIR
    / "data"
    / "product_analytics.duckdb"
)

DASHBOARD_DIR = (
    BASE_DIR
    / "dashboard"
)

DOCS_DIR = (
    BASE_DIR
    / "docs"
)

DASHBOARD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DOCS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# Load dbt product funnel model
# ---------------------------------------------------------

connection = duckdb.connect(
    str(DATABASE_PATH)
)

query = """

SELECT *

FROM main_marts.fct_product_funnel

"""

df = connection.execute(
    query
).fetchdf()

connection.close()


print(
    f"Loaded {len(df):,} customers "
    "from the dbt product funnel model."
)


# ---------------------------------------------------------
# Two-proportion A/B test
# ---------------------------------------------------------

def run_ab_test(
    data,
    outcome,
):
    """
    Compare control and treatment conversion rates
    using a two-proportion z-test.

    Returns:
    - control rate
    - treatment rate
    - absolute lift
    - relative lift
    - confidence interval
    - z statistic
    - p-value
    """

    summary = (
        data
        .groupby("experiment_variant")
        [outcome]
        .agg(
            ["sum", "count"]
        )
    )

    control_successes = int(
        summary.loc[
            "control",
            "sum",
        ]
    )

    treatment_successes = int(
        summary.loc[
            "treatment",
            "sum",
        ]
    )

    control_n = int(
        summary.loc[
            "control",
            "count",
        ]
    )

    treatment_n = int(
        summary.loc[
            "treatment",
            "count",
        ]
    )

    control_rate = (
        control_successes
        / control_n
    )

    treatment_rate = (
        treatment_successes
        / treatment_n
    )


    # Treatment - Control

    absolute_lift = (
        treatment_rate
        - control_rate
    )


    relative_lift = (
        absolute_lift
        / control_rate
    )


    # Statistical significance

    successes = np.array(
        [
            treatment_successes,
            control_successes,
        ]
    )

    observations = np.array(
        [
            treatment_n,
            control_n,
        ]
    )

    z_statistic, p_value = (
        proportions_ztest(
            successes,
            observations,
        )
    )


    # 95% confidence interval for difference
    # in two independent proportions

    standard_error = np.sqrt(

        (
            treatment_rate
            * (1 - treatment_rate)
            / treatment_n
        )

        +

        (
            control_rate
            * (1 - control_rate)
            / control_n
        )
    )

    z_critical = norm.ppf(
        0.975
    )

    confidence_interval_lower = (
        absolute_lift
        - z_critical
        * standard_error
    )

    confidence_interval_upper = (
        absolute_lift
        + z_critical
        * standard_error
    )


    return {

        "metric": outcome,

        "control_users":
            control_n,

        "treatment_users":
            treatment_n,

        "control_rate":
            control_rate,

        "treatment_rate":
            treatment_rate,

        "absolute_lift":
            absolute_lift,

        "relative_lift":
            relative_lift,

        "ci_lower":
            confidence_interval_lower,

        "ci_upper":
            confidence_interval_upper,

        "z_statistic":
            z_statistic,

        "p_value":
            p_value,

        "statistically_significant":
            p_value < 0.05,
    }


# ---------------------------------------------------------
# Overall experiment metrics
# ---------------------------------------------------------

metrics = [

    "recommendation_clicked",

    "activated",

    "application_started",

    "application_completed",
]

experiment_results = []

for metric in metrics:

    result = run_ab_test(
        df,
        metric,
    )

    experiment_results.append(
        result
    )


experiment_results_df = pd.DataFrame(
    experiment_results
)


experiment_results_df.to_csv(

    DASHBOARD_DIR
    / "looker_experiment_summary.csv",

    index=False,
)


# ---------------------------------------------------------
# Segment analysis
# ---------------------------------------------------------

segment_results = []

for dimension in [
    "platform",
    "channel",
]:

    for segment_value in sorted(
        df[dimension]
        .dropna()
        .unique()
    ):

        segment_df = df[
            df[dimension]
            == segment_value
        ]

        result = run_ab_test(
            segment_df,
            "application_completed",
        )

        result[
            "segment_dimension"
        ] = dimension

        result[
            "segment"
        ] = segment_value

        segment_results.append(
            result
        )


segment_results_df = pd.DataFrame(
    segment_results
)


segment_results_df.to_csv(

    DASHBOARD_DIR
    / "looker_segment_results.csv",

    index=False,
)


# ---------------------------------------------------------
# Funnel summary
# ---------------------------------------------------------

funnel_steps = {

    "Signed Up":
        None,

    "Recommendation Clicked":
        "recommendation_clicked",

    "Activated":
        "activated",

    "Application Started":
        "application_started",

    "Application Completed":
        "application_completed",
}


funnel_rows = []

for variant in [
    "control",
    "treatment",
]:

    variant_df = df[
        df["experiment_variant"]
        == variant
    ]

    total_users = len(
        variant_df
    )

    for step_name, column in funnel_steps.items():

        if column is None:

            users = total_users

        else:

            users = int(
                variant_df[column]
                .sum()
            )

        conversion_from_signup = (
            users
            / total_users
        )

        funnel_rows.append(
            {
                "experiment_variant":
                    variant,

                "funnel_step":
                    step_name,

                "users":
                    users,

                "conversion_from_signup":
                    conversion_from_signup,
            }
        )


funnel_df = pd.DataFrame(
    funnel_rows
)


funnel_df.to_csv(

    DASHBOARD_DIR
    / "looker_funnel_summary.csv",

    index=False,
)


# ---------------------------------------------------------
# Console results
# ---------------------------------------------------------

print()
print("=" * 65)
print("OVERALL A/B EXPERIMENT")
print("=" * 65)


for _, row in experiment_results_df.iterrows():

    print()
    print(
        row["metric"]
        .replace("_", " ")
        .title()
    )

    print(
        f"Control: "
        f"{row['control_rate']:.2%}"
    )

    print(
        f"Treatment: "
        f"{row['treatment_rate']:.2%}"
    )

    print(
        f"Absolute lift: "
        f"{row['absolute_lift']:.2%}"
    )

    print(
        f"Relative lift: "
        f"{row['relative_lift']:.2%}"
    )

    print(
        f"95% CI: "
        f"[{row['ci_lower']:.2%}, "
        f"{row['ci_upper']:.2%}]"
    )

    print(
        f"P-value: "
        f"{row['p_value']:.5f}"
    )


# ---------------------------------------------------------
# Product recommendation
# ---------------------------------------------------------

conversion_result = (
    experiment_results_df[
        experiment_results_df[
            "metric"
        ]
        == "application_completed"
    ]
    .iloc[0]
)


significant_segments = (
    segment_results_df[
        segment_results_df[
            "statistically_significant"
        ]
    ]
    .sort_values(
        "absolute_lift",
        ascending=False,
    )
)


if (
    conversion_result[
        "statistically_significant"
    ]
    and
    conversion_result[
        "absolute_lift"
    ] > 0
):

    recommendation = (
        "Proceed with a broader rollout of the "
        "treatment experience while continuing "
        "to monitor conversion and segment-level "
        "performance."
    )

else:

    recommendation = (
        "Do not proceed with a full rollout yet. "
        "Continue testing until the experiment "
        "shows a reliable improvement in "
        "application conversion."
    )


# ---------------------------------------------------------
# Write Product Manager recommendation document
# ---------------------------------------------------------

report_lines = [

    "# Product Experiment Recommendation",
    "",

    "## Executive Summary",
    "",

    (
        f"The treatment experience produced an "
        f"application completion rate of "
        f"**{conversion_result['treatment_rate']:.2%}** "
        f"compared with "
        f"**{conversion_result['control_rate']:.2%}** "
        f"for the control group."
    ),

    "",

    (
        f"This represents an absolute lift of "
        f"**{conversion_result['absolute_lift']:.2%}** "
        f"and a relative lift of "
        f"**{conversion_result['relative_lift']:.2%}**."
    ),

    "",

    (
        f"The 95% confidence interval for the "
        f"conversion difference is "
        f"**{conversion_result['ci_lower']:.2%} to "
        f"{conversion_result['ci_upper']:.2%}**, "
        f"with a p-value of "
        f"**{conversion_result['p_value']:.5f}**."
    ),

    "",

    "## Segment Findings",
    "",
]


for _, row in significant_segments.iterrows():

    report_lines.append(

        (
            f"- **{row['segment']} "
            f"({row['segment_dimension']})**: "
            f"{row['absolute_lift']:.2%} "
            f"absolute conversion lift "
            f"(p={row['p_value']:.4f})."
        )
    )


report_lines.extend(
    [
        "",
        "## Product Recommendation",
        "",
        recommendation,
        "",
        (
            "Segment-level results should be monitored "
            "during rollout because the treatment may "
            "perform differently across acquisition "
            "channels and platforms."
        ),
    ]
)


recommendation_path = (
    DOCS_DIR
    / "product_recommendation.md"
)


recommendation_path.write_text(

    "\n".join(
        report_lines
    ),

    encoding="utf-8",
)


# ---------------------------------------------------------
# Visual 1: overall application conversion
# ---------------------------------------------------------

conversion_rates = (

    df.groupby(
        "experiment_variant"
    )
    ["application_completed"]
    .mean()
    .reindex(
        [
            "control",
            "treatment",
        ]
    )
)


plt.figure(
    figsize=(7, 5)
)

conversion_rates.plot(
    kind="bar"
)

plt.title(
    "Application Completion Rate by Experiment Variant"
)

plt.ylabel(
    "Completion Rate"
)

plt.xlabel(
    "Experiment Variant"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_DIR
    / "application_conversion_by_variant.png",
    dpi=150,
)

plt.close()


# ---------------------------------------------------------
# Visual 2: segment conversion lift
# ---------------------------------------------------------

plot_data = (
    segment_results_df
    .sort_values(
        "absolute_lift",
        ascending=False,
    )
)


plt.figure(
    figsize=(8, 5)
)

plt.bar(
    plot_data["segment"],
    plot_data["absolute_lift"],
)

plt.axhline(
    0,
    linewidth=1,
)

plt.title(
    "Treatment Conversion Lift by Segment"
)

plt.ylabel(
    "Absolute Conversion Lift"
)

plt.xlabel(
    "Segment"
)

plt.xticks(
    rotation=30,
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_DIR
    / "conversion_lift_by_segment.png",
    dpi=150,
)

plt.close()


print()
print("=" * 65)
print("PRODUCT RECOMMENDATION")
print("=" * 65)
print()
print(recommendation)

print()
print(
    "Looker Studio datasets saved in dashboard/."
)

print(
    "Product recommendation saved in docs/."
)
