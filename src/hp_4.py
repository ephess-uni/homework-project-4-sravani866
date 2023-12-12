from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Reformats a list of date strings in format 'yyyy-mm-dd' to 'dd mmm yyyy--01 Jan 2001'."""
    return [datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y") for date in old_dates]

def date_range(start, n):
    """Generates a list of n datetime objects starting at the given start date."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError("Invalid input types.")
    
    return [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i) for i in range(n)]

def add_date_range(values, start_date):
    """Adds a daily date range to the list values beginning with start_date."""
    return [(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i), value) for i, value in enumerate(values)]

def calculate_late_fees(record):
    """Calculates late fees based on the given record."""
    late_fee_days = (datetime.strptime(record['date_returned'], '%m/%d/%Y') - 
                     datetime.strptime(record['date_due'], '%m/%d/%Y')).days
    return round(max(late_fee_days * 0.25, 0), 2)

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to outfile."""
    late_fees_by_patron = defaultdict(float)

    with open(infile) as file:
        reader = DictReader(file)
        for record in reader:
            patron_id = record['patron_id']
            late_fees = calculate_late_fees(record)
            late_fees_by_patron[patron_id] += late_fees

    late_fees_data = [{'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fees)} for patron_id, late_fees in late_fees_by_patron.items()]

    with open(outfile, "w", newline="") as file:
        fieldnames = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(late_fees_data)

# The following main block will run when you choose "Run -> Module" in IDLE.
# Use this section to run test code.

if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')
    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
