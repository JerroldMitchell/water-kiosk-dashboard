#!/usr/bin/env python3
"""
Phase 1: Generate kiosk user/PIN databases
Creates separate user databases for each kiosk with randomized users and PINs
"""

import os
import csv
import random
from pathlib import Path

# ============================================================================
# CONFIGURATION - Adjust these values as needed
# ============================================================================
NUM_KIOSKS = 10  # Number of kiosks to generate
MIN_USERS_PER_KIOSK = 50  # Minimum users per kiosk
MAX_USERS_PER_KIOSK = 100  # Maximum users per kiosk
OUTPUT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # transaction_gen directory

# ============================================================================
# SCRIPT
# ============================================================================

def generate_random_user_id():
    """Generate a random 9-digit Ugandan phone number (708XXXXXX)"""
    return "708" + str(random.randint(100000, 999999))


def generate_random_pin():
    """Generate a random 4-digit PIN"""
    return str(random.randint(1000, 9999))


def generate_random_kiosk_ids(count):
    """Generate random unique 4-digit kiosk IDs"""
    kiosk_ids = set()
    while len(kiosk_ids) < count:
        kiosk_ids.add(random.randint(0, 9999))
    return sorted(list(kiosk_ids))


def generate_kiosk_users(kiosk_id, num_users, num_clients, kiosk_dir):
    """Generate a CSV file with users and PINs for a single kiosk"""
    # Ensure kiosk directory exists
    Path(kiosk_dir).mkdir(parents=True, exist_ok=True)

    # Generate unique user IDs for this kiosk
    users = set()
    while len(users) < num_users:
        users.add(generate_random_user_id())

    # Write user/PIN file
    user_pin_file = os.path.join(kiosk_dir, "kiosk_user_pin.csv")
    with open(user_pin_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['User_ID', 'PIN'])

        for user_id in sorted(users):
            pin = generate_random_pin()
            writer.writerow([user_id, pin])

    # Write metadata file
    metadata_file = os.path.join(kiosk_dir, "kiosk_metadata.csv")
    with open(metadata_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kiosk_ID', 'Num_Clients'])
        writer.writerow([f"{kiosk_id:04d}", num_clients])


def main():
    # Ensure output directory exists
    Path(OUTPUT_DIRECTORY).mkdir(parents=True, exist_ok=True)

    # Generate random kiosk IDs
    kiosk_ids = generate_random_kiosk_ids(NUM_KIOSKS)

    # Generate user/PIN files for each kiosk
    for kiosk_id in kiosk_ids:
        num_users = random.randint(MIN_USERS_PER_KIOSK, MAX_USERS_PER_KIOSK)
        num_clients = random.randint(4, 6)

        kiosk_dir = os.path.join(OUTPUT_DIRECTORY, f"kiosk_{kiosk_id:04d}")
        generate_kiosk_users(kiosk_id, num_users, num_clients, kiosk_dir)


if __name__ == '__main__':
    main()
