---
name: database-schema-validator
description: Validates SQL schema files for compliance with internal safety and naming policies.
---

# Database Schema Validator Skill

This skill checks SQL files against the specific policies listed below. It is a lightweight policy validator, not a full SQL parser.

## Policies Enforced
1. **Safety**: No `DROP TABLE` statements.
2. **Naming**: All tables must use `snake_case`.
3. **Structure**: Every table must have an `id` column as PRIMARY KEY.

## Instructions

1. **Use the validator as the source of truth for the listed automated checks.** Manual review may still be needed for behavior or safety properties outside these rules.
2. **Run the Validation Script**:
   Use the `run_command` tool to execute the python script provided in the `scripts/` folder against the user's file.
   
   ```bash
   python scripts/validate_schema.py <path_to_user_file>
   ```

3. **Interpret Output**:
   - If the script returns **exit code 0**: Tell the user the schema looks good.
   - If the script returns **exit code 1**: Report the specific error messages printed by the script to the user and suggest fixes.


## Limits

A passing result means the listed checks passed for the patterns the validator recognizes. It does not prove the schema is secure, migration-safe, portable across databases, or free of destructive behavior outside those checks.
