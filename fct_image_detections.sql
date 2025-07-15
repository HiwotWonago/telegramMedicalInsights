-- models/facts/fct_image_detections.sql

with detections as (

    select
        image_name,
        detected_object_class,
        confidence_score
    from {{ source('staging', 'image_detections') }}

),

-- Join with fct_messages based on media filename
joined as (

    select
        fm.message_id,
        fm.channel_name,
        fm.media_path,
        d.detected_object_class,
        d.confidence_score
    from {{ ref('fct_messages') }} fm
    join detections d
        on d.image_name = fm.media_path

)

select * from joined
