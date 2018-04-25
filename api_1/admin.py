# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api_1.models import CallSchedule, CallScheduleTimeSlots, CallAppointment


class CallScheduleTimeSlotsInline(admin.TabularInline):
    model = CallScheduleTimeSlots
    extra = 5


class CallScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "confirmed_time", "completed",)
    list_filter = ("completed",)
    inlines = (CallScheduleTimeSlotsInline,)


class CallScheduleTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ("id", "call_schedule", "order", "duration", "time_slot", "accepted",)
    list_filter = ("accepted", "call_schedule",)


class CallAppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "time_slot",)


admin.site.register(CallSchedule, CallScheduleAdmin)
admin.site.register(CallScheduleTimeSlots, CallScheduleTimeSlotsAdmin)
admin.site.register(CallAppointment, CallAppointmentAdmin)
