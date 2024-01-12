from datetime import date, datetime, timedelta
from typing import Tuple


def convert_date_range(start_date: date, end_date: date) -> Tuple[datetime, datetime]:
    """
    Accepts a start_date and end_date and returns corresponding start_datetime and
    returns start_datetime and end_datetime with inclusive start and exclusive stop

    For example:
    (date(2024, 10, 31), date(2024, 12, 12)) => datetime(2024, 10, 31, 0, 0), datetime(2024, 12, 13, 0, 0)
    """
    start_datetime = datetime(start_date.year, start_date.month, start_date.day)
    end_datetime = datetime(
        end_date.year, month=end_date.month, day=end_date.day
    ) + timedelta(days=1)
    return start_datetime, end_datetime
