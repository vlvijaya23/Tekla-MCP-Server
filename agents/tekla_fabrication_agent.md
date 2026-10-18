# Tekla Fabrication Agent

## Agent Name

Tekla Fabrication Agent

---

## Purpose

Convert imported structural members into a fabrication-ready Tekla Structures model.

The agent transforms imported geometry into constructible steelwork suitable for detailing, numbering, drawing production, and fabrication workflows.

---

## Mission

Convert:

```text
Imported Structural Model
```

into:

```text
Fabrication Ready Tekla Model
```

---

## Inputs

### Required

```text
Tekla Model
```

### Required

```text
Imported Members
```

### Optional

```text
STAAD Payload
Profile Mapping
Connection Library
Company Standards
```

---

## Outputs

### Fabrication Model Report

```text
fabrication_model_report.json
```

Example:

```json
{
    "members": 74,
    "columns": 18,
    "beams": 42,
    "braces": 14,
    "status": "fabrication_ready"
}
```

---

### Numbering Report

```text
numbering_report.json
```

Example:

```json
{
    "assemblies": 42,
    "parts": 74
}
```

---

### Connection Report

```text
connection_report.json
```

Example:

```json
{
    "baseplates": 18,
    "beam_connections": 42,
    "brace_connections": 14
}
```

---

## Workflow

```text
Import Members
        |
        V
Validate Geometry
        |
        V
Classify Members
        |
        +---- Column
        |
        +---- Beam
        |
        +---- Brace
        |
        V
Apply Attributes
        |
        V
Apply Numbering
        |
        V
Apply Connections
        |
        V
Generate Drawings
        |
        V
Fabrication Model
```

---

## Member Classification Rules

### Column

```text
dz > max(dx, dy)
```

Classification:

```text
COLUMN
```

---

### Beam

```text
horizontal > 0
and
dz < 20% of horizontal
```

Classification:

```text
BEAM
```

---

### Brace

All remaining members.

Classification:

```text
BRACE
```

---

## Fabrication Standards

### Material

Default:

```text
S355
```

---

### Finish

Default:

```text
PAINT
```

---

### Numbering

```text
Assembly Numbering
Part Numbering
```

must be completed successfully.

---

## Validation Rules

### Geometry Validation

Verify:

```text
No zero-length members
No duplicate members
No invalid geometry
```

---

### Profile Validation

Verify:

```text
Profile exists in Tekla catalog
```

---

### Material Validation

Verify:

```text
Material exists in Tekla catalog
```

---

### Position Validation

Verify:

```text
Plane
Rotation
Depth
```

are valid.

---

## Connection Categories

### Column Base

```text
Base Plate
```

---

### Beam To Column

```text
Shear Connection
```

---

### Beam To Beam

```text
Clip Angle
End Plate
```

---

### Brace Connection

```text
Gusset Plate
```

---

## Drawing Outputs

### GA Drawings

```text
General Arrangement
```

---

### Assembly Drawings

```text
Assembly Shop Drawings
```

---

### Part Drawings

```text
Single Part Drawings
```

---

## Fabrication Readiness Levels

### Level 1

```text
Imported Geometry
```

---

### Level 2

```text
Classified Members
```

---

### Level 3

```text
Numbered Model
```

---

### Level 4

```text
Connected Model
```

---

### Level 5

```text
Fabrication Ready
```

---

## Diagnostics

Track:

```json
{
    "member_id": 100,
    "classification": "COLUMN",
    "profile": "HE220A",
    "material": "S355",
    "status": "validated"
}
```

---

## Success Criteria

The model must satisfy:

```text
All members validated
All profiles resolved
All numbering completed
All connections assigned
```

---

## Current Project Baseline

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

Tekla-MCP-Server 【1-5311aa】

---

## Integration With Other Agents

### Tekla Import Agent

Provides:

```text
Imported Members
```

---

### Geometry Debug Agent

Provides:

```text
Failure Analysis
```

---

### Profile Recovery Agent

Provides:

```text
Profile Mapping
```

---

## Future Enhancements

### Phase 2

```text
Automatic connection placement
```

---

### Phase 3

```text
Automatic numbering
```

---

### Phase 4

```text
Automatic drawing generation
```

---

### Phase 5

```text
Fully autonomous fabrication model generation
```

---

## Long-Term Vision

```text
STAAD
   ↓
Tekla Import Agent
   ↓
Geometry Debug Agent
   ↓
Profile Recovery Agent
   ↓
Tekla Fabrication Agent
   ↓
Fabrication Ready Tekla Model
```