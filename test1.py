from datetime import date, timedelta

def get_previous_month_range():
    today = "2025-03-01"
    print(today)
    if today.day >= 15:
        # Current month is fine
        start_date = date(today.year, today.month - 1, 15) if today.month > 1 else date(today.year - 1, 12, 15)
        end_date = date(today.year, today.month, 14)
    else:
        # Go one more month back
        start_date = date(today.year, today.month - 2, 15) if today.month > 2 else date(today.year - 1, 12 + (today.month - 2), 15)
        end_date = date(today.year, today.month - 1, 14) if today.month > 1 else date(today.year - 1, 12, 14)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

# start, end = get_previous_month_range()
# print(f"{start} to {end}")

from datetime import date, timedelta

def get_previous_month_range(input_date=None):
    """
    Returns the start and end date of the previous month's period.
    - Start date: Always 15th of the previous month.
    - End date: Always 14th of the current month.
    
    If input_date is not provided, it defaults to today's date.
    """
    if input_date is None:
        input_date = date.today()
    print(input_date)
    if input_date.day >= 15:
        # Current month is fine
        start_date = date(input_date.year, input_date.month - 1, 15) if input_date.month > 1 else date(input_date.year - 1, 12, 15)
        end_date = date(input_date.year, input_date.month, 14)
    else:
        # Go one more month back
        start_date = date(input_date.year, input_date.month - 2, 15) if input_date.month > 2 else date(input_date.year - 1, 12 + (input_date.month - 2), 15)
        end_date = date(input_date.year, input_date.month - 1, 14) if input_date.month > 1 else date(input_date.year - 1, 12, 14)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

# Example Usage
custom_date = date(2025, 3, 15)  # Example: Pass a specific date
start, end = get_previous_month_range(custom_date)
print(f"{start} to {end}")

