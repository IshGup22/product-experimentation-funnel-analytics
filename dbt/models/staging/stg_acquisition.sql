WITH source AS (

    SELECT *

    FROM {{ ref('acquisition') }}

),

cleaned AS (

    SELECT

        CAST(acquisition_id AS INTEGER) AS acquisition_id,

        CAST(customer_id AS INTEGER) AS customer_id,

        CAST(acquisition_timestamp AS TIMESTAMP)
            AS acquisition_timestamp,

        LOWER(TRIM(channel)) AS channel,

        LOWER(TRIM(platform)) AS platform,

        LOWER(TRIM(touch_type)) AS touch_type

    FROM source

),

ranked_touchpoints AS (

    SELECT

        *,

        ROW_NUMBER() OVER (

            PARTITION BY customer_id

            ORDER BY
                acquisition_timestamp,
                acquisition_id

        ) AS acquisition_touch_rank,

        COUNT(*) OVER (

            PARTITION BY customer_id

        ) AS total_acquisition_touchpoints

    FROM cleaned

)

SELECT *

FROM ranked_touchpoints
