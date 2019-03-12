from datetime import datetime


def validate_dtformat(date_str: str):
    assert datetime.strptime(
        date_str, "%Y-%m-%d"
    ), "Incorrect data format, should be YYYY-MM-DD"
