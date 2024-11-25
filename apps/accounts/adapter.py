from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from apps.core.functions.calendar import get_calender_list
from apps.google_api.models import GoogleCalendar


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        return super().populate_user(request, sociallogin, data)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        calendar_list = get_calender_list(user)
        print("Calenders: ", calendar_list)
        calc = []
        for calendar in calendar_list:
            print("Data: ", calendar)
            calc.append(
                GoogleCalendar(
                    user=user,
                    kind=calendar["kind"],
                    google_id=calendar["id"],
                    summary=calendar.get("summary", ""),
                    description=calendar.get("description", ""),
                    timezone=calendar["timeZone"],
                    access_role=calendar["accessRole"],
                    primary=calendar.get("primary", False),
                    is_active=calendar.get("primary", False),
                )
            )
        GoogleCalendar.objects.bulk_create(calc)
        return user
