from apps.accounts.models import User
from apps.google_api.models import GoogleCalendar


def get_events(user: User, start_time: str, end_time: str):
    if not user:
        return {"success": False, "error": "User not found"}
    calender_service, message = user.google_calendar
    print("Google Service message: ", message)
    calendar_list = GoogleCalendar.objects.filter(user=user, is_active=True)
    if calender_service:
        result = []
        for calendar in calendar_list:
            response = (
                calender_service.events()
                .list(
                    calendarId=calendar.google_id,
                    timeMin=start_time,
                    timeMax=end_time,
                    orderBy="startTime",
                    showHiddenInvitations=True,
                    singleEvents=True,
                    timeZone=calendar.timezone,
                )
                .execute()
            )
            # print("response: ", response)
            result += response["items"]
        return {"events": result, "success": True}
    return {"success": False, "errors": "Credentials Not Found."}
