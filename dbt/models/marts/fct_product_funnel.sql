WITH customers AS (

    SELECT *

    FROM {{ ref('stg_customers') }}

),

applications AS (

    SELECT *

    FROM {{ ref('stg_applications') }}

),

customer_funnel AS (

    SELECT

        c.customer_id,

        c.signup_date,

        c.experiment_variant,

        a.channel,

        a.platform,

        a.total_acquisition_touchpoints,

        COALESCE(
            app.recommendation_shown,
            0
        ) AS recommendation_shown,

        COALESCE(
            app.recommendation_clicked,
            0
        ) AS recommendation_clicked,

        COALESCE(
            app.activated,
            0
        ) AS activated,

        COALESCE(
            app.application_started,
            0
        ) AS application_started,

        COALESCE(
            app.application_completed,
            0
        ) AS application_completed

    FROM customers c


    LEFT JOIN (

        SELECT *

        FROM {{ ref('stg_acquisition') }}

        WHERE acquisition_touch_rank = 1

    ) a

        ON c.customer_id = a.customer_id


    LEFT JOIN applications app

        ON c.customer_id = app.customer_id

),

final AS (

    SELECT

        *,

        AVG(application_completed) OVER (

            PARTITION BY experiment_variant

        ) AS variant_conversion_rate,

        AVG(application_completed) OVER (

            PARTITION BY channel

        ) AS channel_conversion_rate

    FROM customer_funnel

)

SELECT *

FROM final
