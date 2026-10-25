from tekla_mcp_server import (
    detect_selected_split_columns,
    detect_selected_split_beams,
    merge_safe_column_chains
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

    return (
        merge_safe_column_chains()
    )