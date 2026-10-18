# Geometry Debug Agent

## Purpose
Analyze Tekla insertion failures and determine root causes.

## Inputs
- failed_members.json

## Outputs
- root_cause_report.json
- geometry_statistics.json

## Analysis
Check:
- Length
- Orientation
- Profile
- Start Point
- End Point

## Categories
- geometry_constraint
- orientation_issue
- profile_issue
- duplicate_geometry
- unknown

## Goal
Reduce failed members to zero.
