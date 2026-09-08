WITH source AS (

    SELECT *

    FROM {{ ref('applications') }}

),

cleaned AS (

    SELECT

        CAST(application_id AS INTEGER)
            AS application_id,

        CAST(customer_id AS INTEGER)
            AS customer_id,

        CAST(recommendation_shown AS INTEGER)
            AS recommendation_shown,

        CAST(recommendation_clicked AS INTEGER)
            AS recommendation_clicked,

        CAST(activated AS INTEGER)
            AS activated,

        CAST(application_started AS INTEGER)
            AS application_started,

        CAST(application_completed AS INTEGER)
            AS application_completed,

        CAST(activation_date AS DATE)
            AS activation_date,

        CAST(application_start_date AS DATE)
            AS application_start_date,

        CAST(application_completion_date AS DATE)
            AS application_completion_date

    FROM source

)

SELECT *

FROM cleaned
