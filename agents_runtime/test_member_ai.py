from member_ai import process_member

result = process_member(
    member_id=79,
    profile="L75*75*10",
    start_x=9.175,
    start_y=5.0,
    start_z=0.0,
    end_x=8.150,
    end_y=6.500,
    end_z=0.0
)

from pprint import pprint

pprint(result)