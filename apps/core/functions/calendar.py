from apps.accounts.models import User


def get_calender_list(user: User):
    google_calendar, message = user.google_calendar
    if google_calendar:
        response = google_calendar.calendarList().list(minAccessRole="owner").execute()
        return response["items"]
    return []
