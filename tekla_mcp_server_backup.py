"""
Tekla MCP Server
"""

import os
import sys
import pythonnet
import json
import math

sys.path.append(
    r"C:\tekla-mcp\agents_runtime"
)

from member_ai import process_member

from mcp.server.fastmcp import FastMCP

# ----------------------------------------------------
# MCP SERVER
# ----------------------------------------------------

mcp = FastMCP("tekla")

# ----------------------------------------------------
# TEKLA PATH
# ----------------------------------------------------

TEKLA_BIN = r"C:\TeklaStructures\2025.0\bin"

if not os.path.exists(TEKLA_BIN):
    raise Exception(
        f"Tekla installation not found: {TEKLA_BIN}"
    )

sys.path.append(TEKLA_BIN)

# ----------------------------------------------------
# LOAD PYTHONNET
# ----------------------------------------------------

pythonnet.load("netfx")

import clr

# ----------------------------------------------------
# LOAD TEKLA DLLS
# ----------------------------------------------------

DLLS = [
    "Tekla.Structures.dll",
    "Tekla.Structures.Model.dll",
    "Tekla.Structures.Drawing.dll"
]

for dll in DLLS:

    full_path = os.path.join(
        TEKLA_BIN,
        dll
    )

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Missing DLL: {full_path}"
        )

    print(f"Loading {dll}")

    clr.AddReference(full_path)

# ----------------------------------------------------
# EXTRA REFERENCES
# ----------------------------------------------------

clr.AddReference("Tekla.Structures")

# ----------------------------------------------------
# IMPORTS
# ----------------------------------------------------

from Tekla.Structures.Model import (
    Model,
    ModelObject,
    Beam,
    Position
)

from Tekla.Structures.Geometry3d import (
    Point
)

from Tekla.Structures.Model.UI import (
    ModelObjectSelector
)

print("Tekla assemblies loaded successfully")

from product.core.column_chain_detector import (
    detect_selected_split_columns as detect_column_chains
)

from product.core.column_chain_merger import (
    merge_safe_column_chains as merge_column_chains
)

from product.core.beam_chain_detector import (
    detect_selected_split_beams as detect_beam_chains
)

from product.core.beam_chain_merger import (
    merge_all_safe_beam_chains
)

from product.core.cleanup_engine import (
    cleanup_model
)

# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------

def get_model():

    model = Model()

    if not model.GetConnectionStatus():

        raise Exception(
            "Not connected to Tekla model"
        )

    return model

# ----------------------------------------------------
# PROFILE MAPPING
# ----------------------------------------------------

from core.profile_mapper import (
    map_profile,
    get_all_mappings,
    profile_exists,
    add_profile_mapping
)

def build_column_merge(
    chain_members
):

    merged = dict(
        chain_members[0]
    )

    ys = []

    for member in chain_members:

        ys.append(
            float(
                member["START_Y"]
            )
        )

        ys.append(
            float(
                member["END_Y"]
            )
        )

    merged["START_Y"] = min(
        ys
    )

    merged["END_Y"] = max(
        ys
    )

    return merged

def build_merged_members(
    members
):

    merge_file = (
        r"C:\tekla-mcp\column_merge_candidates.json"
    )

    with open(
        merge_file,
        "r",
        encoding="utf-8"
    ) as f:

        chains = json.load(f)

    member_lookup = {
        m["MEMBER_ID"]: m
        for m in members
    }

    merged_members = []

    merged_ids = set()

    for chain in chains:

        if chain["segment_count"] < 2:
            continue

        chain_members = []

        for member_id in chain["members"]:

            if member_id in member_lookup:

                chain_members.append(
                    member_lookup[
                        member_id
                    ]
                )

        if not chain_members:
            continue

        sample = (
            chain_members[0]
        )

        if (
            sample.get(
                "GROUP",
                ""
            )
            != "_COLUMN"
        ):
            continue

        merged = build_column_merge(
            chain_members
        )

        merged["MEMBER_ID"] = (
            f"MERGED_{chain['members'][0]}"
        )

        merged_members.append(
            merged
        )

        merged_ids.update(
            chain["members"]
        )

    for m in members:

        if (
            m["MEMBER_ID"]
            not in merged_ids
        ):

            merged_members.append(
                m
            )

    return merged_members

def split_long_member(
    member,
    max_length=12.0
):

    dx = (
        float(member["END_X"])
        - float(member["START_X"])
    )

    dy = (
        float(member["END_Y"])
        - float(member["START_Y"])
    )

    dz = (
        float(member["END_Z"])
        - float(member["START_Z"])
    )

    length = (
        dx ** 2 +
        dy ** 2 +
        dz ** 2
    ) ** 0.5

    if length <= max_length:

        return [member]

    count = math.ceil(
        length / max_length
    )

    segments = []

    for i in range(count):

        start_ratio = (
            i * max_length
        ) / length

        end_ratio = min(
            (
                (i + 1)
                * max_length
            ) / length,
            1.0
        )

        segment = dict(member)

        segment["START_X"] = (
            float(member["START_X"])
            + dx * start_ratio
        )

        segment["START_Y"] = (
            float(member["START_Y"])
            + dy * start_ratio
        )

        segment["START_Z"] = (
            float(member["START_Z"])
            + dz * start_ratio
        )

        segment["END_X"] = (
            float(member["START_X"])
            + dx * end_ratio
        )

        segment["END_Y"] = (
            float(member["START_Y"])
            + dy * end_ratio
        )

        segment["END_Z"] = (
            float(member["START_Z"])
            + dz * end_ratio
        )

        segment["MEMBER_ID"] = (
            f"{member['MEMBER_ID']}_S{i+1}"
        )

        segments.append(
            segment
        )

    return segments


def apply_length_limit(
    members
):

    final_members = []

    for member in members:

        final_members.extend(
            split_long_member(
                member,
                12.0
            )
        )

    return final_members

# ----------------------------------------------------
# MCP TOOLS
# ----------------------------------------------------

@mcp.tool()
def selected_column_position():

    selector = (
        ModelObjectSelector()
    )

    selected = (
        selector.GetSelectedObjects()
    )

    result = []

    while selected.MoveNext():

        try:

            beam = (
                selected.Current
            )

            result.append(
                {
                    "id":
                        beam.Identifier.ID,

                    "profile":
                        beam.Profile.ProfileString,

                    "plane":
                        str(
                            beam.Position.Plane
                        ),

                    "rotation":
                        str(
                            beam.Position.Rotation
                        ),

                    "depth":
                        str(
                            beam.Position.Depth
                        )
                }
            )

        except Exception:
            pass

    return result

@mcp.tool()
def selected_member_details():

    selector = (
        ModelObjectSelector()
    )

    selected = (
        selector.GetSelectedObjects()
    )

    result = []

    while selected.MoveNext():

        try:

            beam = (
                selected.Current
            )

            result.append(
                {
                    "id":
                        beam.Identifier.ID,
                    "profile":
                        beam.Profile.ProfileString,
                    "name":
                        beam.Name,
                    "class":
                        beam.Class,
                    "start_x":
                        beam.StartPoint.X,
                    "start_y":
                        beam.StartPoint.Y,
                    "start_z":
                        beam.StartPoint.Z,
                    "end_x":
                        beam.EndPoint.X,
                    "end_y":
                        beam.EndPoint.Y,
                    "end_z":
                        beam.EndPoint.Z
                }
            )

        except Exception:
            pass

    return result

@mcp.tool()
def selected_column_geometry():

    selector = (
        ModelObjectSelector()
    )

    selected = (
        selector.GetSelectedObjects()
    )

    result = []

    while selected.MoveNext():

        try:

            beam = (
                selected.Current
            )

            result.append(
                {
                    "id":
                        beam.Identifier.ID,
                    "profile":
                        beam.Profile.ProfileString,
                    "material":
                        beam.Material.MaterialString,
                    "class":
                        beam.Class,
                    "start_x":
                        beam.StartPoint.X,
                    "start_y":
                        beam.StartPoint.Y,
                    "start_z":
                        beam.StartPoint.Z,
                    "end_x":
                        beam.EndPoint.X,
                    "end_y":
                        beam.EndPoint.Y,
                    "end_z":
                        beam.EndPoint.Z
                }
            )

        except Exception:
            pass

    return result

@mcp.tool()
def selected_column_offsets():

    selector = (
        ModelObjectSelector()
    )

    selected = (
        selector.GetSelectedObjects()
    )

    result = []

    while selected.MoveNext():

        try:

            beam = (
                selected.Current
            )

            result.append(
                {
                    "id":
                        beam.Identifier.ID,

                    "start_offset_x":
                        beam.StartPointOffset.Dx,

                    "start_offset_y":
                        beam.StartPointOffset.Dy,

                    "start_offset_z":
                        beam.StartPointOffset.Dz,

                    "end_offset_x":
                        beam.EndPointOffset.Dx,

                    "end_offset_y":
                        beam.EndPointOffset.Dy,

                    "end_offset_z":
                        beam.EndPointOffset.Dz
                }
            )

        except Exception:
            pass

    return result

@mcp.tool()
def merge_selected_split_columns():

    model = get_model()

    selector = (
        ModelObjectSelector()
    )

    selected = (
        selector.GetSelectedObjects()
    )

    columns = []

    while selected.MoveNext():

        try:

            beam = (
                selected.Current
            )

            if (
                beam.Name.upper()
                != "COLUMN"
            ):
                continue

            columns.append(
                beam
            )

        except Exception:
            pass

    if len(columns) != 2:

        return {
            "status":
                "select_exactly_2_columns"
        }

    col1 = columns[0]
    col2 = columns[1]

    start_point = min(
        [
            col1.StartPoint,
            col1.EndPoint,
            col2.StartPoint,
            col2.EndPoint
        ],
        key=lambda p: p.Z
    )

    end_point = max(
        [
            col1.StartPoint,
            col1.EndPoint,
            col2.StartPoint,
            col2.EndPoint
        ],
        key=lambda p: p.Z
    )

    merged = Beam()

    merged.StartPoint = Point(
        start_point.X,
        start_point.Y,
        start_point.Z
    )

    merged.EndPoint = Point(
        end_point.X,
        end_point.Y,
        end_point.Z
    )

    merged.Profile.ProfileString = (
        col1.Profile.ProfileString
    )

    merged.Material.MaterialString = (
        col1.Material.MaterialString
    )

    merged.Class = (
        col1.Class
    )

    merged.Name = (
        col1.Name
    )

    merged.Position.Plane = (
        col1.Position.Plane
    )

    merged.Position.Rotation = (
        col1.Position.Rotation
    )

    merged.Position.Depth = (
        col1.Position.Depth
    )

    print(
        "BEFORE INSERT",
        str(
            merged.Position.Plane
        ),
        str(
            merged.Position.Rotation
        ),
        str(
            merged.Position.Depth
        )
    )

    success = (
        merged.Insert()
    )

    print(
        "AFTER INSERT",
        str(
            merged.Position.Plane
        ),
        str(
            merged.Position.Rotation
        ),
        str(
            merged.Position.Depth
        )
    )

    merged.Select()

    print(
        "MERGED:",
        str(
            merged.Position.Plane
        ),
        str(
            merged.Position.Rotation
        ),
        str(
            merged.Position.Depth
        )
    )

    if not success:

        return {
            "status":
                "merge_insert_failed"
        }

    col1.Delete()

    col2.Delete()

    model.CommitChanges()

    return {
        "status":
            "merged",
        "profile":
            merged.Profile.ProfileString,
        "length":
            round(
                abs(
                    end_point.Z
                    -
                    start_point.Z
                ),
                2
            )
    }

@mcp.tool()
def is_collinear_beam(
    beam_a,
    beam_b,
    tolerance=0.01
):

    ax = (
        beam_a["end_x"]
        - beam_a["start_x"]
    )

    ay = (
        beam_a["end_y"]
        - beam_a["start_y"]
    )

    az = (
        beam_a["end_z"]
        - beam_a["start_z"]
    )

    bx = (
        beam_b["end_x"]
        - beam_b["start_x"]
    )

    by = (
        beam_b["end_y"]
        - beam_b["start_y"]
    )

    bz = (
        beam_b["end_z"]
        - beam_b["start_z"]
    )

    cross_x = (
        ay * bz
        - az * by
    )

    cross_y = (
        az * bx
        - ax * bz
    )

    cross_z = (
        ax * by
        - ay * bx
    )

    return (
        abs(cross_x) < tolerance
        and abs(cross_y) < tolerance
        and abs(cross_z) < tolerance
    )

@mcp.tool()
def create_span_beams():

    model = get_model()

    from product.core.span_beam_creator import (
        create_span_beams
    )

    return create_span_beams(
        model
    )

@mcp.tool()
def detect_selected_split_beams():

    model = get_model()

    return detect_beam_chains(
        model,
        is_collinear_beam
    )

@mcp.tool()
def detect_selected_split_columns():

    model = get_model()

    return detect_column_chains(
        model
    )

@mcp.tool()
def merge_safe_column_chains():

    model = get_model()

    return merge_column_chains(
        model
    )

@mcp.tool()
def merge_detected_beam_chains():

    model = get_model()

    from product.core.span_beam_creator import (
        create_span_beams
    )

    return create_span_beams(
        model
    )

    result = []

    for item in spans:

        result.append(
            {
                "length":
                    round(
                        item["span"]["length"],
                        0
                    ),

                "beam_count":
                    len(
                        item["beams"]
                    )
            }
        )

    return result

@mcp.tool()
def get_model_info():

    model = get_model()

    info = model.GetInfo()

    return {
        "model_name": info.ModelName,
        "model_path": info.ModelPath
    }


@mcp.tool()
def count_beams():

    model = get_model()

    selector = model.GetModelObjectSelector()

    beams = selector.GetAllObjectsWithType(
        ModelObject.ModelObjectEnum.BEAM
    )

    count = 0

    while beams.MoveNext():
        count += 1

    return count


@mcp.tool()
def list_beam_profiles_unique(limit: int = 200):

    model = get_model()

    selector = model.GetModelObjectSelector()

    beams = selector.GetAllObjectsWithType(
        ModelObject.ModelObjectEnum.BEAM
    )

    profiles = set()

    while beams.MoveNext():

        beam = beams.Current

        try:

            profiles.add(
                beam.Profile.ProfileString
            )

        except Exception:
            pass

        if len(profiles) >= limit:
            break

    return sorted(list(profiles))


@mcp.tool()
def selected_count():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    count = 0

    while selected.MoveNext():
        count += 1

    return count


@mcp.tool()
def selected_profiles():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    profiles = []

    while selected.MoveNext():

        obj = selected.Current

        try:

            profile = obj.Profile.ProfileString

            if profile not in profiles:
                profiles.append(profile)

        except Exception:
            pass

    return profiles


@mcp.tool()
def selected_objects():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    result = []

    while selected.MoveNext():

        obj = selected.Current

        try:

            result.append(
                {
                    "id": obj.Identifier.ID,
                    "profile": obj.Profile.ProfileString
                }
            )

        except Exception:
            pass

    return result


@mcp.tool()
def create_beam(
    profile: str,
    start_x: float,
    start_y: float,
    start_z: float,
    end_x: float,
    end_y: float,
    end_z: float,
    name: str = "SACS_BEAM",
    phase: str = "UNCLASSIFIED"
):

    try:

        model = get_model()

        beam = Beam()

        beam.StartPoint = Point(
            start_x * 1000.0,
            start_z * 1000.0,
            start_y * 1000.0
        )

        beam.EndPoint = Point(
            end_x * 1000.0,
            end_z * 1000.0,
            end_y * 1000.0
        )

        beam.Profile.ProfileString = profile
        member_ai = process_member(
            member_id=0,
            profile=profile,
            start_x=start_x,
            start_y=start_y,
            start_z=start_z,
            end_x=end_x,
            end_y=end_y,
            end_z=end_z
        )
        
        beam.Material.MaterialString = (
            member_ai["classification"]["material"]
        )

        beam.Class = (
            member_ai["classification"]["class"]
        )

        phase = (
            member_ai["classification"]["phase"]
        )

        member_type = (
            member_ai["classification"]["member_type"]
        )

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        dz = abs(end_z - start_z)

        horizontal = max(dx, dy)

        #
        # Naming
        #

        if member_type == "COLUMN":

            beam.Name = "COLUMN"

        else:

            beam.Name = "BEAM"

        #
        # Position
        #

        beam.Position.Plane = (
            Position.PlaneEnum.MIDDLE
        )

        if member_type == "COLUMN":

            beam.Position.Rotation = (
                Position.RotationEnum.FRONT
            )

            beam.Position.Depth = (
                Position.DepthEnum.MIDDLE
            )

        else:

            beam.Position.Rotation = (
                Position.RotationEnum.TOP
            )

            beam.Position.Depth = (
                Position.DepthEnum.BEHIND
            )

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        dz = abs(end_z - start_z)

        horizontal = max(dx, dy)

        length = (
            (end_x - start_x) ** 2 +
            (end_y - start_y) ** 2 +
            (end_z - start_z) ** 2
        ) ** 0.5

        if length < 0.25:

            return {
                "status": "short_member",
                "length": length,
                "profile": profile,
                "name": beam.Name
            }

        success = beam.Insert()

        if success:

            model.CommitChanges()

            print(
                f"SUCCESS | {name} | "
                f"({start_x:.3f}, {start_y:.3f}, {start_z:.3f}) -> "
                f"({end_x:.3f}, {end_y:.3f}, {end_z:.3f})"
            )

            return {
                "status": "success",
                "name": beam.Name,
                "profile": profile,
                "phase": phase,
                "class": beam.Class
            }

        return {
            "status": "insert_failed",
            "name": beam.Name,
            "profile": profile,
            "length": length,
            "start": [
                start_x,
                start_y,
                start_z
            ],
            "end": [
                end_x,
                end_y,
                end_z
            ]
        }

    except Exception as ex:

        return {
            "status": "exception",
            "error": str(ex),
            "name": name,
            "profile": profile
        }

def audit_model(
    members
):

    audit = {
        "health_score": 100,
        "split_columns": [],
        "beam_gaps": [],
        "profile_changes": [],
        "tiny_members": [],
        "duplicate_members": []
    }

    for member in members:

        dx = (
            float(member["END_X"])
            - float(member["START_X"])
        )

        dy = (
            float(member["END_Y"])
            - float(member["START_Y"])
        )

        dz = (
            float(member["END_Z"])
            - float(member["START_Z"])
        )

        length = (
            dx ** 2 +
            dy ** 2 +
            dz ** 2
        ) ** 0.5

        if length < 0.25:

            audit[
                "tiny_members"
            ].append(
                {
                    "member":
                        member[
                            "MEMBER_ID"
                        ],
                    "profile":
                        member[
                            "PROFILE"
                        ],
                    "length":
                        round(
                            length,
                            3
                        )
                }
            )

    profile_map = {}

    for member in members:

        if (
            member.get(
                "GROUP",
                ""
            )
            != "_COLUMN"
        ):
            continue

        x = round(
            float(
                member["START_X"]
            ),
            3
        )

        z = round(
            float(
                member["START_Z"]
            ),
            3
        )

        key = (
            x,
            z
        )

        if key not in profile_map:

            profile_map[key] = set()

        profile_map[key].add(
            member["PROFILE"]
        )

    for location, profiles in profile_map.items():

        if len(
            profiles
        ) > 1:

            audit[
                "profile_changes"
            ].append(
                {
                    "location":
                        location,
                    "profiles":
                        list(
                            profiles
                        )
                }
            )

    beam_members = []

    for member in members:

        if (
            member.get(
                "GROUP",
                ""
            )
            == "_COLUMN"
        ):
            continue

        beam_members.append(
            member
        )

    for beam_a in beam_members:

        for beam_b in beam_members:

            if (
                beam_a[
                    "MEMBER_ID"
                ]
                ==
                beam_b[
                    "MEMBER_ID"
                ]
            ):
                continue

            gap = abs(
                float(
                    beam_a[
                        "END_X"
                    ]
                )
                -
                float(
                    beam_b[
                        "START_X"
                    ]
                )
            )

            if (
                gap > 0.01
                and
                gap < 0.30
            ):

                audit[
                    "beam_gaps"
                ].append(
                    {
                        "member_a":
                            beam_a[
                                "MEMBER_ID"
                            ],
                        "member_b":
                            beam_b[
                                "MEMBER_ID"
                            ],
                        "gap":
                            round(
                                gap,
                                3
                            )
                    }
                )


    column_locations = {}

    for member in members:

        if (
            member.get(
                "GROUP",
                ""
            )
            != "_COLUMN"
        ):
            continue

        x = round(
            float(
                member["START_X"]
            ),
            3
        )

        z = round(
            float(
                member["START_Z"]
            ),
            3
        )

        key = (
            x,
            z
        )

        if key not in column_locations:

            column_locations[key] = []

        column_locations[key].append(
            member
        )

    for location, chain in column_locations.items():

        if len(chain) > 1:

            profiles = {
                m["PROFILE"]
                for m in chain
            }

            if len(profiles) > 1:

                audit[
                    "split_columns"
                ].append(
                    {
                        "location":
                            location,
                        "profiles":
                            list(
                                profiles
                            ),
                        "member_count":
                            len(
                                chain
                            )
                    }
                )

    issue_count = (
        len(
            audit[
                "split_columns"
            ]
        )
        +
        len(
            audit[
                "profile_changes"
            ]
        )
        +
        len(
            audit[
                "beam_gaps"
            ]
        )
    )

    audit[
        "health_score"
    ] = max(
        0,
        100 - (
            issue_count * 10
        )
    )

    return audit

def finalize_audit(
    audit
):

    finalizer = {
        "auto_fixed": [],
        "review_required": []
    }

    for member in audit[
        "tiny_members"
    ]:

        finalizer[
            "auto_fixed"
        ].append(
            {
                "type":
                    "TINY_MEMBER",
                "member":
                    member[
                        "member"
                    ],
                "profile":
                    member[
                        "profile"
                    ],
                "action":
                    "SAFE_TO_IGNORE"
            }
        )

    for beam in audit[
        "beam_gaps"
    ]:

        finalizer[
            "review_required"
        ].append(
            {
                "type":
                    "BEAM_GAP",
                "member_a":
                    beam[
                        "member_a"
                    ],
                "member_b":
                    beam[
                        "member_b"
                    ],
                "gap":
                    beam[
                        "gap"
                    ],
                "action":
                    "MERGE_RECOMMENDED"
            }
        )

    for column in audit[
        "split_columns"
    ]:

        profiles = (
            column[
                "profiles"
            ]
        )

        recommended_profile = (
            profiles[0]
        )

        confidence = (
            "MEDIUM"
        )

        if (
            "HE220A"
            in profiles
        ):

            recommended_profile = (
                "HE220A"
            )

            confidence = (
                "HIGH"
            )

        finalizer[
            "review_required"
        ].append(
            {
                "type":
                    "SPLIT_COLUMN",
                "location":
                    column[
                        "location"
                    ],
                "profiles":
                    profiles,
                "recommended_profile":
                    recommended_profile,
                "confidence":
                    confidence,
                "action":
                    "REVIEW_REQUIRED"
            }
        )

    return finalizer

@mcp.tool()
def import_staad_json(
    json_file: str = r"C:\TeklaAssistant\data\staad_payload.json",
    limit: int = 10,
    progress_callback=None
):

    try:

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:

            payload = json.load(f)

        members = payload.get(
            "members",
            []
        )

        audit = audit_model(
            members
        )

        finalizer = (
            finalize_audit(
                audit
            )
        )

        with open(
            r"C:\tekla-mcp\finalizer_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                finalizer,
                f,
                indent=4
            )

        with open(
            r"C:\tekla-mcp\model_audit.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                audit,
                f,
                indent=4
            )

        members = build_merged_members(
            members
        )

        members = apply_length_limit(
            members
        )

        if limit > 0:

            members = members[:limit]

        created = 0
        failed = 0
        skipped = 0
        skipped_members = []
        errors = []

        total_members = len(
            members
        )

        for index, member in enumerate(
            members,
            start=1
        ):

            try:

                profile = map_profile(
                    member["PROFILE"]
                )

                result = create_beam(
                    profile=profile,
                    start_x=float(member["START_X"]),
                    start_y=float(member["START_Y"]),
                    start_z=float(member["START_Z"]),
                    end_x=float(member["END_X"]),
                    end_y=float(member["END_Y"]),
                    end_z=float(member["END_Z"]),
                    name=f"STAAD_{member['MEMBER_ID']}",
                    phase=member["GROUP"]
                )

                status = result.get("status")

                if status == "success":

                    created += 1

                elif status == "short_member":

                    skipped += 1

                    skipped_members.append(
                        {
                            "member": member["MEMBER_ID"],
                            "profile": member["PROFILE"],
                            "reason": "Length < 250 mm",
                            "length": result.get(
                                "length",
                                0
                            )
                        }
                    )

                else:

                    failed += 1

                    errors.append(
                        {
                            "member": member["MEMBER_ID"],
                            "profile": member["PROFILE"],
                            "result": result
                        }
                    )

                if progress_callback:

                    progress = int(
                        (
                            index
                            / total_members
                        ) * 100
                    )

                    progress_callback(
                        progress
                    )

            except Exception as ex:

                failed += 1

                errors.append(
                    {
                        "member": member.get(
                            "MEMBER_ID",
                            "UNKNOWN"
                        ),
                        "profile": member.get(
                            "PROFILE",
                            "UNKNOWN"
                        ),
                        "error": str(ex)
                    }
                )

                if progress_callback:

                    progress = int(
                        (
                            index
                            / total_members
                        ) * 100
                    )

                    progress_callback(
                        progress
                    )

        with open(
            r"C:\tekla-mcp\failed_members.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                errors,
                f,
                indent=4
            )

        profile_summary = {}

        for error in errors:

            profile = error.get(
                "profile",
                "UNKNOWN"
            )

            profile_summary[
                profile
            ] = (
                profile_summary.get(
                    profile,
                    0
                ) + 1
            )

        with open(
            r"C:\tekla-mcp\skipped_members.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                skipped_members,
                f,
                indent=4
            )

        return {
            "status": "completed",
            "created": created,
            "failed": failed,
            "skipped": skipped,
            "total": len(members),
            "errors": errors,
            "skipped_members": skipped_members
        }

    except Exception as ex:

        return {
            "status": "exception",
            "error": str(ex)
        }

@mcp.tool()
def auto_cleanup_model():

    model = get_model()

    return cleanup_model(
        model,
        is_collinear_beam
    )

@mcp.tool()
def test_beam_spans():

    model = get_model()

    from product.core.beam_span_builder import (
        build_beam_spans
    )

    spans = build_beam_spans(
        model
    )

    result = []

    for item in spans:

        span = item["span"]

        result.append(
            {
                "start_column":
                    span["start_column"],

                "end_column":
                    span["end_column"],

                "length":
                    round(
                        span["length"],
                        0
                    ),

                "beam_count":
                    len(
                        item["beams"]
                    )
            }
        )

    return result

# ----------------------------------------------------
# MAIN
# ----------------------------------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test",
        action="store_true"
    )

    args = parser.parse_args()

    if args.test:

        print("Testing Tekla Connection...")

        print()

        print("Model Info:")
        print(get_model_info())

        print()

        print("Beam Count:")
        print(count_beams())

        print()

        print("Selected Count:")
        print(selected_count())

        print()

        print("Profiles:")
        print(
            list_beam_profiles_unique(200)
        )

        print()

        print("Create Test Beam: SKIPPED")

        print()

        print("Selected Member Details:")
        print()

        result = (
            selected_column_offsets()
        )

        print(
            json.dumps(
                result,
                indent=4
            )
        )

    else:

        print()
        print("===================================")
        print("Starting Tekla MCP Server...")
        print("===================================")
        print()

        try:

            mcp.run()

        except Exception as ex:

            print()
            print("===================================")
            print("MCP SERVER ERROR")
            print("===================================")
            print()

            print(str(ex))

            print()

            input("Press Enter to close...")


