
from datetime import datetime, timedelta


def get_utc_date():
    """
    returns the date 3 hours ago
    :return:
    """
    # Get current UTC time
    current_utc_time = datetime.utcnow()

    # Format the result in yyyy-mm-dd format
    formatted_time = current_utc_time.strftime('%Y-%m-%d')
    datetime.utcnow().strftime('%Y-%m-%d')
    return formatted_time


def get_utc_date_1_hours_ago(current_utc_time=None):
    if not current_utc_time:
        # Get current UTC time
        current_utc_time = datetime.utcnow()

    # Calculate the time 30 minutes ago
    time_30_minutes_ago = current_utc_time - timedelta(hours=3)
    # Format the result in yyyy-mm-dd format
    formatted_time = time_30_minutes_ago.strftime('%Y-%m-%d')

    return formatted_time


def get_custom_timestamps():
    # Get the current timestamp
    current_timestamp = datetime.utcnow()

    # Calculate the first timestamp (multiple of half hours preceding current time - 30 mins)
    # get the nearest hour of the current timestamp
    first_timestamp = current_timestamp.replace(minute=0, second=0, microsecond=0)
    if current_timestamp.minute <= 30:
        first_timestamp -= timedelta(minutes=30)

    # Calculate the second timestamp (3 hours earlier than the first timestamp)
    second_timestamp = first_timestamp - timedelta(hours=3)

    # Format the timestamps in the specified format (yyyy-mm-dd hh:mm:ss)
    first_timestamp_str = first_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    second_timestamp_str = second_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    # current_timestamp_str = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    # print(current_timestamp_str)
    return first_timestamp_str, second_timestamp_str


def time_to_next_run():
    """
    returns the time to next big query sync
    :return: time_in_seconds
    """
    now = datetime.utcnow()
    next_cron_job = now.replace(hour=0, minute=45, second=0, microsecond=0)

    # Calculate the time to the next cron job
    while now >= next_cron_job:
        next_cron_job += timedelta(hours=3)

    time_difference = next_cron_job - now
    time_in_seconds = time_difference.total_seconds()

    return time_in_seconds


# # Example usage
# seconds_to_next_cron_job = time_to_next_run()
# print(f"Time to the next cron job: {seconds_to_next_cron_job} seconds")