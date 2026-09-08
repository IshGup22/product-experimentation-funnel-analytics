WITH funnel AS (

    SELECT *

    FROM {{ ref('fct_product_funnel') }}

),

aggregated AS (

    SELECT

        experiment_variant,

        platform,

        channel,

        COUNT(*) AS users,

        SUM(recommendation_shown)
            AS recommendations_shown,

        SUM(recommendation_clicked)
            AS recommendation_clicks,

        SUM(activated)
            AS activated_users,

        SUM(application_started)
            AS application_starts,

        SUM(application_completed)
            AS application_completions

    FROM funnel

    GROUP BY

        experiment_variant,

        platform,

        channel

)

SELECT

    *,

    ROUND(
        recommendation_clicks * 1.0
        / NULLIF(recommendations_shown, 0),
        4
    ) AS recommendation_ctr,

    ROUND(
        activated_users * 1.0
        / NULLIF(users, 0),
        4
    ) AS activation_rate,

    ROUND(
        application_starts * 1.0
        / NULLIF(users, 0),
        4
    ) AS application_start_rate,

    ROUND(
        application_completions * 1.0
        / NULLIF(users, 0),
        4
    ) AS application_completion_rate

FROM aggregated
