WITH experiment_funnel AS (

    SELECT

        experiment_variant,

        COUNT(*) AS users,

        SUM(recommendation_clicked)
            AS recommendation_clicks,

        SUM(activated)
            AS activated_users,

        SUM(application_started)
            AS application_starts,

        SUM(application_completed)
            AS completed_applications

    FROM marts.fct_product_funnel

    GROUP BY experiment_variant

)

SELECT

    experiment_variant,

    users,

    recommendation_clicks,

    activated_users,

    application_starts,

    completed_applications,

    ROUND(
        recommendation_clicks * 1.0
        / users,
        4
    ) AS recommendation_ctr,

    ROUND(
        activated_users * 1.0
        / users,
        4
    ) AS activation_rate,

    ROUND(
        application_starts * 1.0
        / users,
        4
    ) AS application_start_rate,

    ROUND(
        completed_applications * 1.0
        / users,
        4
    ) AS application_completion_rate

FROM experiment_funnel

ORDER BY experiment_variant;
