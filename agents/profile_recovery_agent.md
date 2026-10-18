# Profile Recovery Agent

## Agent Name

Profile Recovery Agent

---

## Purpose

Identify unsupported STAAD profiles and automatically determine the best Tekla profile equivalent.

The objective is to maximize structural recovery during STAAD → Tekla import.

---

## Mission

Convert:

```text
Unknown STAAD Profile
```

into:

```text
Valid Tekla Profile
```

while preserving structural intent.

---

## Inputs

### Required

```text
staad_payload.json
```

### Required

```text
failed_members.json
```

### Optional

```text
profile_statistics.json
PROFILE_MAP
Tekla Catalog Export
```

---

## Outputs

### Recovery Report

```text
profile_recovery_report.json
```

Example:

```json
{
    "staad_profile": "L75X75X10",
    "tekla_profile": "L75*75*10",
    "status": "mapped"
}
```

---

### Unresolved Profiles

```text
unknown_profiles.json
```

Example:

```json
[
    "CUSTOM_PROFILE_1",
    "PIPE_SPECIAL_200"
]
```

---

### Mapping Recommendations

```text
profile_mapping_recommendations.json
```

Example:

```json
{
    "100X6.3SHS": "SHS100*100*6.3",
    "L100X100X10": "L100*100*10"
}
```

---

## Workflow

```text
Read STAAD Payload
          |
          V
Extract Profiles
          |
          V
Compare Against PROFILE_MAP
          |
          +---- Found
          |         |
          |         V
          |      Approved
          |
          +---- Missing
                    |
                    V
          Search Tekla Catalog
                    |
                    +---- Match Found
                    |         |
                    |         V
                    |      Recommend Mapping
                    |
                    +---- No Match
                              |
                              V
                       Unknown Profile
```

---

## Supported Profile Families

### I Sections

```text
HEA
HEB
HEM
HE
IPE
IPN
UB
UC
```

---

### Channels

```text
UPN
UPE
PFC
MC
```

---

### Angles

```text
L
EA
```

---

### Hollow Sections

```text
SHS
RHS
CHS
PIPE
TUBE
```

---

### Plates

```text
PL
PLATE
```

---

## Mapping Rules

### Angle Conversion

Convert:

```text
L75X75X10
```

To:

```text
L75*75*10
```

---

### SHS Conversion

Convert:

```text
100X6.3SHS
```

To:

```text
SHS100*100*6.3
```

---

### Tube Conversion

Convert:

```text
TUBE TH 0.012 WT 0.22 DT 0.21
```

To:

```text
Equivalent RHS or SHS
```

when available.

---

### Preserve Native Profiles

Keep:

```text
HE160A
HE220A
UPN140
```

unchanged if available in Tekla.

---

## Recovery Categories

### Native Match

```text
native_match
```

Example:

```text
HE220A
```

---

### Direct Mapping

```text
direct_mapping
```

Example:

```text
L100X100X10 → L100*100*10
```

---

### Family Mapping

```text
family_mapping
```

Example:

```text
PIPE → CHS
```

---

### Substitute Mapping

```text
substitute_mapping
```

Example:

```text
Unknown RHS → nearest RHS
```

---

### Unresolved

```text
unresolved
```

---

## Confidence Levels

### High

```text
Exact profile found
```

---

### Medium

```text
Same family profile
```

---

### Low

```text
Nearest equivalent profile
```

---

## Validation Rules

Before accepting a mapping:

```text
1. Profile exists in Tekla catalog
2. Profile inserts successfully
3. Dimensions are compatible
4. Section family is preserved
```

---

## Success Criteria

The agent must:

```text
Reduce profile-related failures
```

while preserving structural intent.

---

## Current Known Mappings

```json
{
    "HE220A": "HE220A",
    "HE160A": "HE160A",
    "UPN140": "UPN140",
    "L75X75X10": "L75*75*10",
    "L100X100X10": "L100*100*10",
    "100X6.3SHS": "SHS100*100*6.3"
}
```

---

## Current Project Status

```text
Total Members : 157
Created       : 74
Skipped       : 36
Failed        : 47
```

Current Branch:

```text
geometry-debug
```

Repository:

```text
Tekla-MCP-Server
```

---

## Future Enhancements

### Phase 2

```text
Automatic catalog lookup
```

### Phase 3

```text
Automatic profile testing
```

### Phase 4

```text
Machine-learned profile recovery
```

### Phase 5

```text
Autonomous STAAD profile translation
```