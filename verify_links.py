import os
from datetime import datetime, timedelta

def pad(num):
    return f"{num:02d}"

def check_files():
    current_date = datetime.now()
    # Fixed date for testing to match user's context if needed, but user said "now"
    # User time: 2025-11-26
    current_date = datetime(2025, 11, 26)
    
    year = current_date.year
    month = current_date.month
    day = current_date.day
    
    print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")

    # Check MC
    mc_suffix = f"{pad(month)}{pad(day)}"
    mc_file = f"mccheyne/mc{mc_suffix}.html"
    if os.path.exists(mc_file):
        print(f"[OK] MC file exists: {mc_file}")
    else:
        print(f"[FAIL] MC file missing: {mc_file}")

    # Check DB
    year_suffix = str(year)[-2:]
    db_suffix = f"{year_suffix}{pad(month)}{pad(day)}"
    db_file = f"dailybible/db{db_suffix}.html"
    if os.path.exists(db_file):
        print(f"[OK] DB file exists: {db_file}")
    else:
        print(f"[FAIL] DB file missing: {db_file}")

    # Check Catechism (day)
    dc_suffix = f"{pad(month)}{pad(day)}"
    dc_file = f"catechism/dc{dc_suffix}.html"
    if os.path.exists(dc_file):
        print(f"[OK] Catechism file exists: {dc_file}")
    else:
        print(f"[FAIL] Catechism file missing: {dc_file}")

    # Check Sermon
    # Calculate last Sunday
    # Sunday is 6 in Python's weekday() where Mon=0, Sun=6?
    # No, Python weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    # JS getDay(): Sun=0, Mon=1, ...
    
    # JS logic: date.getDate() - date.getDay()
    # If Wed (JS=3), date - 3.
    # Python: Wed=2.
    # We need to replicate JS logic exactly.
    
    # JS: Sun=0, Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6
    js_day_of_week = (current_date.weekday() + 1) % 7
    
    last_sunday = current_date - timedelta(days=js_day_of_week)
    
    sermon_year_suffix = str(last_sunday.year)[-2:]
    sermon_date_suffix = f"{sermon_year_suffix}{pad(last_sunday.month)}{pad(last_sunday.day)}"
    
    print(f"Last Sunday: {last_sunday.strftime('%Y-%m-%d')}")
    
    prefixes = ['ae', 'ms', 'as']
    for prefix in prefixes:
        sermon_file = f"sermon/{prefix}{sermon_date_suffix}.html"
        if os.path.exists(sermon_file):
            print(f"[OK] Sermon file exists: {sermon_file}")
        else:
            print(f"[FAIL] Sermon file missing: {sermon_file}")

if __name__ == "__main__":
    check_files()
