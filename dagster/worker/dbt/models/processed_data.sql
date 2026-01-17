select * 
from {{ source('raw', 'raw_data') }}
where _timestamp > {{ var('min_date') }}
    and _timestamp < {{ var('max_date') }}