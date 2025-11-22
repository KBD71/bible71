import os
import sys
import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily override datetime for testing
original_datetime = datetime.datetime

class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        # Return tomorrow's date (2025-11-23)
        return original_datetime(2025, 11, 23, 10, 0, 0)

# Monkey patch
datetime.datetime = MockDatetime

# Import and run the main script
from bot import main

if __name__ == "__main__":
    main()
