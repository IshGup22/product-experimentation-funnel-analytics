WITH segment_performance AS (

    SELECT

        experiment_variant,

        platform,

        channel,

        COUNT(*) AS users,

        SUM(application_completed)
            AS completed_applications

    FROM marts.fct_product_funnel

    GROUP BY

        experiment_variant,

        platform,

        channel

),

conversion_rates AS (

    SELECT

        experiment_variant,

        platform,

        channel,

        users,

        completed_applications,

        completed_applications * 1.0
            / NULLIF(users, 0)
            AS conversion_rate

    FROM segment_performance

)

SELECT

    experiment_variant,

    platform,

    channel,

    users,

    completed_applications,

    ROUND(
        conversion_rate,
        4
    ) AS conversion_rate,

    RANK() OVER (

        PARTITION BY experiment_variant

        ORDER BY conversion_rate DESC

    ) AS segment_conversion_rank

FROM conversion_rates

ORDER BY

    experiment_variant,

    segment_conversion_rank;
