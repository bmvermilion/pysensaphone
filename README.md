# pysensaphone

A Python library for interacting with the Sensaphone Sentinel REST API, specifically designed to automate and protect the Melody Woods Water Company's distribution system.

## Overview
This library provides a high-level interface for controlling Sentinel devices via their REST API. It abstracts away the raw HTTP requests and session management, providing specialized logic for water system operations such as pump control, tank level monitoring, and automated safety shutoffs.

## Key Features
- **Session Management**: Automated login with a KMS-encrypted credential file and token caching in AWS SSM Parameter Store to prevent API throttling.
- **Shared Helpers**: Pacific-time handling, device/zone lookup, SSM parameter access, tank-level parsing, and timer/daily-window checks used by the Lambda handlers.
- **Safety Interlocks**: Built-in `DRY_RUN` support to simulate operations without triggering physical relays.
- **Email Alert Parser**: Extraction of device names, power status, and chlorine alarms from Sensaphone notification emails.

## Core Modules
- `sensaphone_auth`: Authentication using AWS KMS and SSM caching.
- `get_sensaphone`: Retrieves system status, device info, and sensor data.
- `set_sensaphone`: Modifies device outputs (e.g., toggling pump relays).
- `water_logic`: Shared timezone, lookup, parsing, and scheduling helpers.
- `email_parser`: Parses alert emails (power/chlorine).
- `exceptions`: Base exception types for the library.

## Environment
- `SENSAPHONE_USERNAME`: Sensaphone login name. Defaults to the Melody Woods WorkMail address.
- `SENSAPHONE_CACHE_PARAMETER`: SSM parameter used for the session cache (default `/sensaphone/session`).
- `DRY_RUN`: Set to `true` to log intended output changes instead of writing them.
- `AWS_EXECUTION_ENV`: When set (Lambda), sessions are cached in SSM; otherwise the library uses a local `creds.json`.

The credential file `pysensaphone/encrypted_controls.pem` is KMS ciphertext and requires `kms:Decrypt` on the configured key in `us-east-1`.

## Deployment
This library is intended to be deployed as an **AWS Lambda Layer**. The layer is vendored into the `melodywoods_water` repo; update it there by running `make sync-layer`, `make build` and `make deploy` from that repo's root.

## License

GPL-2.0. See [LICENSE](LICENSE).
