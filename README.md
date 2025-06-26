# Bitcoin Transaction Analyzer

This project analyzes Bitcoin blockchain transactions using Google BigQuery. It focuses on filtering specific transaction types, such as HTLC (Hashed Timelock Contracts), and tracking blockchain data for research or monitoring purposes.

## Features
- Connects to Google BigQuery to query Bitcoin blockchain data.
- Filters and identifies HTLC transactions.
- Tracks last synced block for incremental analysis.
- Includes utilities for parsing, logging, and wallet address handling.

## Files Overview
- `bigquery.py` / `new bigquery.py`: Query and process data from BigQuery.
- `filter HTLC.py`: Detects HTLC-related transactions.
- `wallet.py`: Handles wallet-related operations.
- `last_sync_block.txt`: Stores the latest processed block number.
- `utils.py`, `parser_utils.py`, `logger.py`: Utility and helper functions.
- `config.py`: Project configuration settings.

## Requirements
- Python 3.x
- Google Cloud SDK / credentials for BigQuery access

## How to Run
1. Install dependencies.
2. Set up your Google Cloud credentials.
3. Run the desired script (e.g., `python bigquery.py`).

<br>
author-aanya katiyar
