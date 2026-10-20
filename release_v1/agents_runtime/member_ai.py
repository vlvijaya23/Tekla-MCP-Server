from classification_agent import classify_member
from naming_agent import generate_name
from position_agent import get_position_rule
from quality_agent import evaluate_member


def process_member(
    member_id,
    profile,
    start_x,
    start_y,
    start_z,
    end_x,
    end_y,
    end_z
):

    classification = classify_member(
        profile,
        start_x,
        start_y,
        start_z,
        end_x,
        end_y,
        end_z
    )

    name = generate_name(
        classification["member_type"],
        member_id
    )

    position = get_position_rule(
        classification["member_type"],
        profile
    )

    quality = evaluate_member(
        profile,
        start_x,
        start_y,
        start_z,
        end_x,
        end_y,
        end_z
    )

    return {
        "member_id": member_id,
        "name": name,
        "classification": classification,
        "position": position,
        "quality": quality
    }


if __name__ == "__main__":

    result = process_member(
        79,
        "L75*75*10",
        0,
        0,
        0,
        5,
        5,
        0
    )

    from pprint import pprint

    pprint(result)