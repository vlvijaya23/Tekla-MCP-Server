# Tekla Import Agent

## Purpose
Import STAAD members into Tekla Structures.

## Inputs
- staad_payload.json
- profile mappings

## Outputs
- import_summary.json
- failed_members.json
- profile_statistics.json

## Workflow
Read STAAD Payload
Map Profiles
Validate Length
Create Tekla Members
Record Failures
Generate Reports

## Success Criteria
Created + Failed + Skipped = Total
