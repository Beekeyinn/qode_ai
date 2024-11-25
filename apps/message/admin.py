from django.contrib import admin

from apps.message.models import Message, Thread


# Register your models here.
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user", "assistant", "thread_id"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ["thread", "message", "role", "message_id"]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
