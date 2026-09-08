from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SEED = 42
N_CUSTOMERS = 20_000

BASE_DIR = Path(__file__).resolve().parents[1]
SEED_DIR = BASE_DIR / "dbt" / "seeds"

SEED_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(SEED)


# ---------------------------------------------------------
# 1. Customer data
# ---------------------------------------------------------

customer_id = np.arange(1, N_CUSTOMERS + 1)

experiment_variant = rng.choice(
    ["control", "treatment"],
    size=N_CUSTOMERS,
    p=[0.50, 0.50],
)

primary_channel = rng.choice(
    ["paid_social", "search", "referral"],
    size=N_CUSTOMERS,
    p=[0.35, 0.40, 0.25],
)

primary_platform = rng.choice(
    ["mobile", "web"],
    size=N_CUSTOMERS,
    p=[0.62, 0.38],
)

signup_offsets = rng.integers(0, 90, size=N_CUSTOMERS)

signup_dates = (
    pd.Timestamp("2026-01-01")
    + pd.to_timedelta(signup_offsets, unit="D")
)

customers = pd.DataFrame(
    {
        "customer_id": customer_id,
        "signup_date": signup_dates,
        "experiment_variant": experiment_variant,
    }
)


# ---------------------------------------------------------
# 2. Product recommendation interaction
# ---------------------------------------------------------

# Treatment represents a personalized recommendation experience.
# Control represents the standard experience.

recommendation_click_probability = (
    0.24
    + (experiment_variant == "treatment") * 0.045
    + (primary_channel == "referral") * 0.025
    + (primary_channel == "search") * 0.010
    + (primary_platform == "web") * 0.010
)

recommendation_clicked = (
    rng.random(N_CUSTOMERS)
    < recommendation_click_probability
)


# ---------------------------------------------------------
# 3. Activation
# ---------------------------------------------------------

activation_probability = (
    0.54
    + (experiment_variant == "treatment") * 0.030
    + recommendation_clicked * 0.070
    + (primary_platform == "web") * 0.020
    + (primary_channel == "referral") * 0.030
    - (primary_channel == "paid_social") * 0.015
)

activated = (
    rng.random(N_CUSTOMERS)
    < activation_probability
)


# ---------------------------------------------------------
# 4. Application start
# ---------------------------------------------------------

application_start_probability = (
    0.56
    + (experiment_variant == "treatment") * 0.020
    + (primary_channel == "referral") * 0.030
    + (primary_platform == "web") * 0.010
)

application_started = (
    activated
    & (
        rng.random(N_CUSTOMERS)
        < application_start_probability
    )
)


# ---------------------------------------------------------
# 5. Application completion
# ---------------------------------------------------------

application_completion_probability = (
    0.61
    + (experiment_variant == "treatment") * 0.040
    + (primary_channel == "search") * 0.020
    + (primary_channel == "referral") * 0.040
    - (primary_platform == "mobile") * 0.015
)

application_completed = (
    application_started
    & (
        rng.random(N_CUSTOMERS)
        < application_completion_probability
    )
)


# ---------------------------------------------------------
# 6. Acquisition data
# ---------------------------------------------------------

first_touch_dates = (
    signup_dates
    - pd.to_timedelta(
        rng.integers(4, 11, size=N_CUSTOMERS),
        unit="D",
    )
)

acquisition_records = []

acquisition_id = 1

for i in range(N_CUSTOMERS):
    acquisition_records.append(
        {
            "acquisition_id": acquisition_id,
            "customer_id": int(customer_id[i]),
            "acquisition_timestamp": first_touch_dates[i],
            "channel": primary_channel[i],
            "platform": primary_platform[i],
            "touch_type": "first_touch",
        }
    )

    acquisition_id += 1


# Add additional marketing touchpoints for some users.
# This gives us a realistic reason to use SQL window functions
# to identify the first acquisition source.

extra_indices = rng.choice(
    np.arange(N_CUSTOMERS),
    size=int(N_CUSTOMERS * 0.30),
    replace=False,
)

for i in extra_indices:

    extra_channel = rng.choice(
        ["paid_social", "search", "referral"]
    )

    extra_timestamp = (
        signup_dates[i]
        - pd.to_timedelta(
            rng.integers(0, 4),
            unit="D",
        )
    )

    acquisition_records.append(
        {
            "acquisition_id": acquisition_id,
            "customer_id": int(customer_id[i]),
            "acquisition_timestamp": extra_timestamp,
            "channel": extra_channel,
            "platform": primary_platform[i],
            "touch_type": "additional_touch",
        }
    )

    acquisition_id += 1


acquisition = pd.DataFrame(acquisition_records)


# ---------------------------------------------------------
# 7. Application data
# ---------------------------------------------------------

activation_delay = rng.integers(
    0,
    4,
    size=N_CUSTOMERS,
)

activation_dates = []

application_start_dates = []

application_completion_dates = []

for i in range(N_CUSTOMERS):

    if activated[i]:

        activation_date = (
            signup_dates[i]
            + pd.Timedelta(
                days=int(activation_delay[i])
            )
        )

        activation_dates.append(
            activation_date
        )

    else:

        activation_dates.append(
            pd.NaT
        )


    if application_started[i]:

        start_date = (
            activation_dates[i]
            + pd.Timedelta(
                days=int(
                    rng.integers(0, 3)
                )
            )
        )

        application_start_dates.append(
            start_date
        )

    else:

        application_start_dates.append(
            pd.NaT
        )


    if application_completed[i]:

        completion_date = (
            application_start_dates[i]
            + pd.Timedelta(
                days=int(
                    rng.integers(0, 4)
                )
            )
        )

        application_completion_dates.append(
            completion_date
        )

    else:

        application_completion_dates.append(
            pd.NaT
        )


applications = pd.DataFrame(
    {
        "application_id": np.arange(
            1,
            N_CUSTOMERS + 1
        ),
        "customer_id": customer_id,
        "recommendation_shown": 1,
        "recommendation_clicked": recommendation_clicked.astype(int),
        "activated": activated.astype(int),
        "application_started": application_started.astype(int),
        "application_completed": application_completed.astype(int),
        "activation_date": activation_dates,
        "application_start_date": application_start_dates,
        "application_completion_date": application_completion_dates,
    }
)


# ---------------------------------------------------------
# 8. Save datasets as dbt seeds
# ---------------------------------------------------------

customers.to_csv(
    SEED_DIR / "customers.csv",
    index=False,
)

acquisition.to_csv(
    SEED_DIR / "acquisition.csv",
    index=False,
)

applications.to_csv(
    SEED_DIR / "applications.csv",
    index=False,
)


print("Synthetic product analytics data created successfully.")
print()
print(f"Customers: {len(customers):,}")
print(f"Acquisition touchpoints: {len(acquisition):,}")
print(f"Applications: {len(applications):,}")
print()
print(f"Files saved to: {SEED_DIR}")
