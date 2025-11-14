# Transaction Generation Scripts

This directory contains Python scripts to generate synthetic kiosk user databases and transaction files for testing and development purposes.

## Overview

The scripts generate realistic water dispenser kiosk data with:
- Multiple kiosks with randomized IDs (0000-9999)
- Independent user databases per kiosk
- Realistic transaction data with timestamps, volume consumption, and response status
- Abuse detection test cases (5% of users exceeding daily limits)

## Directory Structure

Each script creates and maintains a directory structure:

```
transaction_gen/
├── generate_kiosk_users.py       # Phase 1: Generate kiosk databases
├── generate_transactions.py      # Phase 2: Generate transaction files
├── README.md                     # This file
└── kiosk_XXXX/                   # One directory per kiosk
    ├── kiosk_metadata.csv        # Kiosk configuration (ID, num clients)
    ├── kiosk_user_pin.csv        # User database (User_ID, PIN)
    └── transactions_XXXX_MMDDYY.csv  # Daily transaction files (30 files)
```

## Phase 1: Generate Kiosk User Databases

### Script: `generate_kiosk_users.py`

Generates user and PIN databases for multiple kiosks.

#### Configuration (top of script)

```python
NUM_KIOSKS = 10              # Number of kiosks to generate
MIN_USERS_PER_KIOSK = 50     # Minimum users per kiosk
MAX_USERS_PER_KIOSK = 100    # Maximum users per kiosk
OUTPUT_DIRECTORY = ...       # Where to generate kiosk directories
```

#### Running the Script

```bash
python3 generate_kiosk_users.py
```

#### Output

Creates 10 directories with randomized kiosk IDs:
- `kiosk_0604/`, `kiosk_1505/`, `kiosk_2413/`, etc.

Each directory contains:
- **kiosk_metadata.csv** - Single row with:
  - `Kiosk_ID`: 4-digit randomized ID
  - `Num_Clients`: 4-6 clients for this kiosk (consistent for all transactions)

- **kiosk_user_pin.csv** - User database with:
  - `User_ID`: 9-digit Ugandan phone numbers (708XXXXXX)
  - `PIN`: 4-digit random PIN per user

#### Example Output

```
kiosk_metadata.csv:
Kiosk_ID,Num_Clients
0604,4

kiosk_user_pin.csv:
User_ID,PIN
708137368,5293
708141817,7368
708169819,2313
```

## Phase 2: Generate Transaction Files

### Script: `generate_transactions.py`

Generates daily transaction files for each kiosk based on the user databases created in Phase 1.

#### Configuration (top of script)

```python
NUM_DAYS = 30                              # Days of transactions to generate
MIN_VOLUME_ML = 100                        # Min volume per transaction
MAX_VOLUME_ML = 600                        # Max volume per transaction
NORMAL_USER_MAX_DAILY_VOLUME = 1500        # Max daily volume for normal users (1.5L)
ABUSIVE_USER_MAX_DAILY_VOLUME = 3000       # Max daily volume for abusive users (3L)
ABUSIVE_USER_PERCENTAGE = 0.05             # 5% of users are abusive
NORMAL_USER_TRANSACTIONS_PER_DAY = 3       # Expected transactions per normal user
ABUSIVE_USER_MIN_TRANSACTIONS_PER_DAY = 5  # Min transactions for abusive users
ABUSIVE_USER_MAX_TRANSACTIONS_PER_DAY = 7  # Max transactions for abusive users
PASS_PERCENTAGE = 0.98                     # 98% PASS, 2% FAIL responses
```

#### Running the Script

```bash
python3 generate_transactions.py
```

#### Output

For each kiosk, generates 30 daily transaction files (by default):
- `transactions_0604_101525.csv`, `transactions_0604_101625.csv`, ..., `transactions_0604_111325.csv`

Each file contains transaction records with:
- `Timestamp`: Date and time (YYYY-MM-DD HH:MM:SS, 6 AM - 6 PM)
- `Client_Name`: Client 1-N (N depends on kiosk's Num_Clients)
- `User_ID`: 9-digit Ugandan phone number
- `PIN`: User's 4-digit PIN
- `Volume_ML`: Transaction volume (100-600 ML)
- `Response`: PASS or FAIL

#### Example Transaction File

```
Timestamp,Client_Name,User_ID,PIN,Volume_ML,Response
2025-10-15 06:05:41,Client 2,708304699,6785,144,PASS
2025-10-15 06:06:02,Client 3,708902536,2007,341,PASS
2025-10-15 06:14:40,Client 2,708213559,1426,171,PASS
2025-10-15 06:39:31,Client 2,708871149,8159,182,PASS
```

## Data Characteristics

### User Distribution
- **50-100 users per kiosk** (randomized)
- **Unique user sets per kiosk** (no overlap between kiosks)
- **5% abusive users** (2-5 users per kiosk)

### Normal Users
- ~3 transactions per day (±1)
- Max 1500 ML (1.5 L) per day
- Mostly PASS responses

### Abusive Users (Detection Testing)
- 5-7 transactions per day
- Max 3000 ML (3 L) per day
- Marked for system abuse detection testing

### Transaction Timestamps
- Generated for last 30 days (Oct 15 - Nov 13, 2025)
- Times between 6:00 AM and 6:00 PM
- Randomized within each day
- Sorted chronologically within each file

### Clients Per Kiosk
- **Consistent**: Each kiosk has 4-6 clients (fixed at generation time)
- **Persistent**: Number stored in kiosk_metadata.csv, survives transaction regeneration
- **Used in all transactions**: All 30 days use same client set for that kiosk

## Workflow Example

### Step 1: Generate Kiosk Databases

```bash
python3 generate_kiosk_users.py
```

Creates 10 kiosks with users and metadata.

### Step 2: Generate Transactions

```bash
python3 generate_transactions.py
```

Generates 30 days of transactions for each kiosk.

### Step 3: Regenerate Transactions (Optional)

To regenerate transactions while keeping kiosk configuration (users, clients):

```bash
# Delete old transaction files while keeping kiosk directories
rm -f kiosk_*/transactions_*.csv

# Regenerate transactions
python3 generate_transactions.py
```

The kiosk configuration (users, PINs, client count) will remain unchanged because it's stored in the kiosk directories.

## Customization

### Add More Kiosks

Edit `generate_kiosk_users.py`:
```python
NUM_KIOSKS = 20  # Generate 20 kiosks instead of 10
```

Then run:
```bash
python3 generate_kiosk_users.py
```

### Adjust Number of Days

Edit `generate_transactions.py`:
```python
NUM_DAYS = 60  # Generate 60 days instead of 30
```

Then regenerate transactions:
```bash
rm -f kiosk_*/transactions_*.csv
python3 generate_transactions.py
```

### Change User Range Per Kiosk

Edit `generate_kiosk_users.py`:
```python
MIN_USERS_PER_KIOSK = 100   # Minimum 100 users
MAX_USERS_PER_KIOSK = 150   # Maximum 150 users
```

Then regenerate:
```bash
rm -rf kiosk_*
python3 generate_kiosk_users.py
python3 generate_transactions.py
```

### Adjust Volume Parameters

Edit `generate_transactions.py`:
```python
MIN_VOLUME_ML = 150        # Minimum 150 ML per transaction
MAX_VOLUME_ML = 800        # Maximum 800 ML per transaction
NORMAL_USER_MAX_DAILY_VOLUME = 2000  # Increase daily limit to 2L
```

Then regenerate transactions:
```bash
rm -f kiosk_*/transactions_*.csv
python3 generate_transactions.py
```

## Notes

- **User IDs are Ugandan phone numbers** starting with 708 (e.g., 708137368)
- **Timestamps are realistic** for testing analytics and time-based queries
- **Daily volume limits are enforced** to create realistic usage patterns
- **Abusive users intentionally exceed limits** to test detection logic
- **All data is synthetic** for testing and development only
- **Kiosk IDs are randomized** (0000-9999) to simulate distributed deployments

## Requirements

- Python 3.x
- Standard library only (csv, os, datetime, random, pathlib)

## Troubleshooting

### "No kiosk_* directories found"

Make sure you ran `generate_kiosk_users.py` first to create the kiosk directories.

### "ValueError: empty range for randrange()"

This was a volume allocation bug that has been fixed. Make sure you're using the latest version of the scripts.

### Transaction files not generating

Check that:
1. Kiosk directories exist with `kiosk_metadata.csv` and `kiosk_user_pin.csv`
2. No permission errors writing to kiosk directories
3. Sufficient disk space for 30 files per kiosk
