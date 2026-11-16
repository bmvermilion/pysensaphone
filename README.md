# pysensaphone

A Python library for interacting with the Sensaphone Sentinel REST API, specifically designed to automate and protect the Melody Woods Water Company's distribution system.

## Overview
This library provides a high-level interface for controlling Sentinel devices via their REST API. It abstracts away the raw HTTP requests and session management, providing specialized logic for water system operations such as pump control, tank level monitoring, and automated safety shutoffs.

## Key Features
- **Session Management**: Automated login with KMS-encrypted credentials and efficient token caching in AWS SSM Parameter Store to prevent API throttling.
- **Water Logic Engine**: Standardized rules for 88k tank optimization (High/Noon/Morning windows), Well #3 timer windows, and unit-aware parsing (e.g., converting "22.5 Ft" to float).
- **Safety Interlocks**: Built-in `DRY_RUN` support to simulate operations without triggering physical relays.
- **Email Alert Parser**: Robust extraction of device names, power status, and chlorine alarms from Sensaphone notification emails.

## Core Modules
- `sensaphone_auth`: Authentication logic using AWS KMS and SSM caching.
- `get_sensaphone`: Retrieves system status, device info, and sensor data.
- `set_sensaphone`: Modifies device outputs (e.g., toggling pump relays).
- `water_logic`: Centralized business rules and formatting utilities.
- `email_parser`: Logic for reacting to emergency alerts (Power/Chlorine).

## Deployment
This library is intended to be deployed as an **AWS Lambda Layer**. To update the shared library across all system functions, modify the code here and run `make build` and `make deploy` from the project root.
