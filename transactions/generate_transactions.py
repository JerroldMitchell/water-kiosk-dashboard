#!/usr/bin/env python3
"""
Phase 2: Generate transaction CSV files for each kiosk
Creates daily transaction files based on kiosk user databases
"""

import os
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURATION - Adjust these values as needed
# ============================================================================
NUM_DAYS = 30  # Number of days of transactions to generate
OUTPUT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # transaction_gen directory
MIN_VOLUME_ML = 100
MAX_VOLUME_ML = 600
NORMAL_USER_MAX_DAILY_VOLUME = 1500
ABUSIVE_USER_MAX_DAILY_VOLUME = 3000
ABUSIVE_USER_PERCENTAGE = 0.05
NORMAL_USER_TRANSACTIONS_PER_DAY = 3
NORMAL_USER_TRANSACTION_VARIANCE = 1  # ±1 transaction
ABUSIVE_USER_MIN_TRANSACTIONS_PER_DAY = 5
ABUSIVE_USER_MAX_TRANSACTIONS_PER_DAY = 7
PASS_PERCENTAGE = 0.98  # 98% PASS, 2% FAIL

# ============================================================================
# SCRIPT
# ============================================================================

def get_kiosk_directories(output_dir):
    """Find all kiosk directories"""
    kiosk_dirs = []
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.path.isdir(item_path) and item.startswith("kiosk_"):
            kiosk_dirs.append(item_path)
    return sorted(kiosk_dirs)


def extract_kiosk_id(directory_path):
    """Extract kiosk ID from directory path like /path/to/kiosk_1234"""
    dirname = os.path.basename(directory_path)
    return dirname.split('_')[1]  # Return the XXXX from kiosk_XXXX


def load_kiosk_metadata(kiosk_dir):
    """Load kiosk metadata from kiosk directory"""
    metadata_file = os.path.join(kiosk_dir, "kiosk_metadata.csv")

    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"kiosk_metadata.csv not found in {kiosk_dir}")

    with open(metadata_file, 'r') as f:
        reader = csv.DictReader(f)
        row = next(reader)
        kiosk_id = row['Kiosk_ID']
        num_clients = int(row['Num_Clients'])

    return kiosk_id, num_clients


def load_kiosk_users(kiosk_dir):
    """Load users and PINs from kiosk directory, return dict of {user_id: pin}"""
    users = {}
    user_pin_file = os.path.join(kiosk_dir, "kiosk_user_pin.csv")

    if not os.path.exists(user_pin_file):
        raise FileNotFoundError(f"kiosk_user_pin.csv not found in {kiosk_dir}")

    with open(user_pin_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['User_ID']] = row['PIN']
    return users


def identify_abusive_users(users, percentage):
    """Randomly identify a percentage of users as abusive"""
    user_list = list(users.keys())
    num_abusive = max(1, int(len(user_list) * percentage))
    abusive = set(random.sample(user_list, num_abusive))
    return abusive


def generate_random_time_between(start_hour, end_hour):
    """Generate random time between start and end hour"""
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def generate_transactions_for_day(date, users, abusive_users, num_clients):
    """Generate transactions for a single day"""
    transactions = []

    # Use the fixed number of clients for this kiosk
    clients_today = [f"Client {i}" for i in range(1, num_clients + 1)]

    # Track volume per user
    user_volumes = defaultdict(int)

    # Decide which users will have transactions today
    user_list = list(users.keys())
    num_users_active = random.randint(
        max(1, len(user_list) // 3),  # At least 1/3 of users
        len(user_list)  # At most all users
    )
    active_users = random.sample(user_list, num_users_active)

    # Generate transactions for each active user
    for user_id in active_users:
        is_abusive = user_id in abusive_users

        # Determine number of transactions for this user today
        if is_abusive:
            num_transactions = random.randint(
                ABUSIVE_USER_MIN_TRANSACTIONS_PER_DAY,
                ABUSIVE_USER_MAX_TRANSACTIONS_PER_DAY
            )
        else:
            num_transactions = max(1, random.randint(
                NORMAL_USER_TRANSACTIONS_PER_DAY - NORMAL_USER_TRANSACTION_VARIANCE,
                NORMAL_USER_TRANSACTIONS_PER_DAY + NORMAL_USER_TRANSACTION_VARIANCE
            ))

        pin = users[user_id]
        max_allowed = ABUSIVE_USER_MAX_DAILY_VOLUME if is_abusive else NORMAL_USER_MAX_DAILY_VOLUME

        # Generate transactions for this user
        for _ in range(num_transactions):
            current_volume = user_volumes[user_id]
            remaining_volume = max_allowed - current_volume

            if remaining_volume < MIN_VOLUME_ML:
                break  # User hit daily limit or doesn't have enough for minimum transaction

            # Generate volume
            volume = random.randint(MIN_VOLUME_ML, min(MAX_VOLUME_ML, remaining_volume))
            user_volumes[user_id] += volume

            # Random time between 6 AM and 6 PM
            time_str = generate_random_time_between(6, 18)
            timestamp = f"{date} {time_str}"

            # Random client
            client = random.choice(clients_today)

            # Response - mostly PASS
            response = "PASS" if random.random() < PASS_PERCENTAGE else "FAIL"

            transactions.append({
                'Timestamp': timestamp,
                'Client_Name': client,
                'User_ID': user_id,
                'PIN': pin,
                'Volume_ML': volume,
                'Response': response
            })

    # Sort by timestamp to maintain chronological order
    transactions.sort(key=lambda x: x['Timestamp'])

    return transactions


def generate_kiosk_transactions(kiosk_id, users, num_clients, kiosk_dir):
    """Generate all days of transactions for a kiosk"""
    # Identify abusive users
    abusive_users = identify_abusive_users(users, ABUSIVE_USER_PERCENTAGE)

    # Get date range (last NUM_DAYS from today)
    today = datetime(2025, 11, 13)
    start_date = today - timedelta(days=NUM_DAYS - 1)

    for i in range(NUM_DAYS):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        date_file_str = current_date.strftime("%m%d%y")

        # Generate transactions
        transactions = generate_transactions_for_day(date_str, users, abusive_users, num_clients)

        # Write to CSV in kiosk directory
        filename = os.path.join(kiosk_dir, f"transactions_{kiosk_id}_{date_file_str}.csv")
        with open(filename, 'w', newline='') as f:
            if transactions:
                writer = csv.DictWriter(f, fieldnames=['Timestamp', 'Client_Name', 'User_ID', 'PIN', 'Volume_ML', 'Response'])
                writer.writeheader()
                writer.writerows(transactions)


def main():
    # Ensure output directory exists
    Path(OUTPUT_DIRECTORY).mkdir(parents=True, exist_ok=True)

    # Find all kiosk directories
    kiosk_dirs = get_kiosk_directories(OUTPUT_DIRECTORY)

    if not kiosk_dirs:
        print("Error: No kiosk_* directories found in output directory")
        return

    # Generate transactions for each kiosk
    for kiosk_dir in kiosk_dirs:
        try:
            kiosk_id, num_clients = load_kiosk_metadata(kiosk_dir)
            users = load_kiosk_users(kiosk_dir)

            print(f"Generating transactions for kiosk {kiosk_id} ({len(users)} users, {num_clients} clients)...")
            generate_kiosk_transactions(kiosk_id, users, num_clients, kiosk_dir)
        except FileNotFoundError as e:
            print(f"Warning: {e}, skipping kiosk directory {os.path.basename(kiosk_dir)}")
            continue

    print("Done!")


if __name__ == '__main__':
    main()
