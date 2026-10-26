from tekla_mcp_server import (
    detect_selected_split_columns,
    detect_selected_split_beams,
    merge_safe_column_chains,
    merge_detected_beam_chains
)


def detect_members():

    result = []

    result.extend(
        detect_selected_split_columns()
    )

    result.extend(
        detect_selected_split_beams()
    )

    return result


def merge_members():

    column_result = (
        merge_safe_column_chains()
    )

    beam_result = (
        merge_detected_beam_chains()
    )

    return {
        "columns":
            column_result,

        "beams":
            beam_result
    }