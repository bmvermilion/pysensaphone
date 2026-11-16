# pysensaphone

A Python library for interacting with the Sensaphone Sentinel REST API, specifically tailored for the Melody Woods Water Company infrastructure.

## Key Features
- **Session Caching**: Reduces API calls by caching session tokens in AWS SSM Parameter Store.
- **Water Logic Engine**: Shared utilities for tank level parsing, 15-minute schedule window checks, and device discovery.
- **Safety Interlocks**: Integrated support for Dry Run modes and safety-first pump control.
- **Email Parsing**: Dedicated parser for Sensaphone alert emails (Power/Chlorine).

## Modules
- `sensaphone_auth`: Handles KMS-encrypted login and SSM session caching.
- `get_sensaphone`: Low-level REST API requests and system status retrieval.
- `set_sensaphone`: Controls Sentinel relay outputs.
- `water_logic`: High-level business rules for water production.
- `email_parser`: Extracts actionable data from alert emails.

## Development
This library is deployed as an **AWS Lambda Layer**.

1. Update code in `pysensaphone/`.
2. Run `make build` and `make deploy` from the root directory to update the shared Layer across all Lambda functions.
