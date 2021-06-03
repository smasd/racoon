from datetime import datetime
import pytz
import tzlocal


def convert_to_ltz(timestamp, format):
    return datetime.strptime(timestamp, format).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime(
        "%Y-%m-%d %H:%M")
