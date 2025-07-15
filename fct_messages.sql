-- models/facts/fct_messages.sql

with messages as (

    select
        message_id,
        message_timestamp,
        channel_name,
        sender,
        message,
        length(message) as message_length,
        media_type,
        media_path,
        case when media_type is not null then true else false end as has_media

    from {{ ref('stg_telegram_messages') }}

),

final as (

    select
        message_id,
        message_timestamp,
        channel_name,
        sender,
        message,
        message_length,
        media_type,
        media_path,
        has_media

    from messages

)

select * from final
