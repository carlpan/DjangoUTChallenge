# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from pytz import UnknownTimeZoneError
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from api_1.models import CallSchedule, CallScheduleTimeSlots, CallAppointment

TIME_ZONE = "America/Los_Angeles"


"""
Imagine you are using a scheduling system to schedule a call with someone.
The system requires user to suggest three times, the user can then remove the times.
When a time is removed, user can then add a new time to keep three call times.
For the sake of writing unit tests, the user can also accept the time. When a call is 
accepted, a signal (in signals.py) is triggered to create a call appointment entry in database.
Please go to route /call_schedules/ to play with the flow.
Please also refer to admin page for model definitions.
"""


def conference_call_schedules(request):
    """
    Main call scheduling api handles create new call schedules
    and rendering existing call schedules and appointments.
    """
    if request.method == 'GET':
        context = build_call_schedule_data()
        return render(request, "call_schedule.html", context)
    else:
        identifier = request.POST.get("identifier", None)
        if identifier:
            try:
                call_schedule = CallSchedule.objects.get(id=int(identifier))
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Call schedule missing")
        else:
            call_schedule = CallSchedule.objects.create(created_on=timezone.now())
        call_schedule.call_schedule_time_slots.all().delete()

        num_options = 3
        for i in range(1, num_options + 1):
            duration = request.POST.get("duration%s" % i)
            time_slot = request.POST.get("datetime%s" % i)

            # Calculate time slot
            f_str = '%m/%d/%Y %H:%M'
            selected_date = datetime.strptime(time_slot, f_str)
            selected_date_utc = convert_to_utc(selected_date, TIME_ZONE)

            CallScheduleTimeSlots.objects.create(
                call_schedule=call_schedule,
                order=i,
                duration=duration,
                time_slot=selected_date_utc
            )

        # Build data for template
        context = build_call_schedule_data()
        template = loader.get_template("call_schedule_detail.html")
        return HttpResponse(template.render(context))


def accept_remove_time_slot(request):
    """
    Handles accept and remove a time slot in an existing call schedule.
    """
    if request.method == 'POST':
        identifier = request.POST.get("identifier", None)
        order = request.POST.get("order", None)
        is_for_accept = int(request.POST.get("for_accept"))

        if not identifier and not order:
            return HttpResponseBadRequest("Missing identifier and call time slot order")

        try:
            call_schedule = CallSchedule.objects.get(id=identifier)
            time_slot = call_schedule.call_schedule_time_slots.get(order=order)

            if is_for_accept:
                time_slot.accepted = True
                time_slot.save()
                call_schedule.completed = True
                call_schedule.confirmed_time = time_slot.time_slot
                call_schedule.save()
            else:
                time_slot.delete()

            # Build data for template
            context = build_call_schedule_data()
            template = loader.get_template("call_schedule_detail.html")
            return HttpResponse(template.render(context))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Call schedule or time slot missing")
        except MultipleObjectsReturned:
            return HttpResponseBadRequest("Multiple call schedules or time slots returned!")


def add_single_time_slot(request):
    """
    Handles adding a time slot to an existing call schedule.
    """
    identifier = request.POST.get("identifier", None)

    latest_call_time_order = 1
    try:
        call_schedule = CallSchedule.objects.get(id=identifier)
        latest_call_times = call_schedule.call_schedule_time_slots.all().order_by("-order")
        if latest_call_times:
            latest_call_time = latest_call_times[0]
            latest_call_time_order = latest_call_time.order + 1
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Call schedule missing")

    duration = request.POST.get("duration1")
    time_slot = request.POST.get("datetime1")

    # Calculate time slot
    f_str = '%m/%d/%Y %H:%M'
    selected_date = datetime.strptime(time_slot, f_str)
    selected_date_utc = convert_to_utc(selected_date, TIME_ZONE)

    CallScheduleTimeSlots.objects.create(
        call_schedule=call_schedule,
        order=latest_call_time_order,
        duration=duration,
        time_slot=selected_date_utc
    )

    # Build data for template
    context = build_call_schedule_data()
    template = loader.get_template("call_schedule_detail.html")
    return HttpResponse(template.render(context))


###########
# Helpers #
###########

def build_call_schedule_data():
    """
    Construct existing call schedule and appointments data.
    """
    # Build proposed time slots data
    time_slot_data = list()
    call_schedules = CallSchedule.objects.filter(completed=False).order_by("-created_on")
    has_call_schedule = False  # has current pending call schedule
    call_schedule_id = None
    if call_schedules:
        has_call_schedule = True
        call_schedule = call_schedules[0]
        call_schedule_id = call_schedule.id
        proposed_time_slots = call_schedule.call_schedule_time_slots.all().order_by("order")
        for time_slot in proposed_time_slots:
            time_slot_local = convert_to_timezone(time_slot.time_slot, TIME_ZONE)
            time_info_part_1 = time_slot_local.strftime('%-H:%M')
            time_info_part_2 = time_slot_local.strftime('%B %d, %Y')
            timezone_shorthand = shorten_timezone_name(time_slot_local, TIME_ZONE)
            time_slot_data.append({
                "id": time_slot.id,
                "order": time_slot.order,
                "timezone": TIME_ZONE,
                "duration": time_slot.duration,
                "time_info_1": time_info_part_1,
                "time_info_2": time_info_part_2,
                "timezone_shorthand": timezone_shorthand
            })

    # Build call appointments
    scheduled_call_appointments = CallAppointment.objects.all().order_by("time_slot")
    call_appointments_data = list()
    for call_appointment in scheduled_call_appointments:
        time_slot_local = convert_to_timezone(call_appointment.time_slot, TIME_ZONE)
        time_slot_local_formatted = time_slot_local.strftime('%m/%d/%y')
        call_appointments_data.append({
            'time_slot_local': time_slot_local_formatted
        })

    # Build context
    context = {
        'has_call_schedule': has_call_schedule,
        'call_schedule_identifier': call_schedule_id,
        'time_slots': time_slot_data,
        'scheduled_call_appointments': call_appointments_data
    }

    return context


def convert_to_timezone(date, tz):
    """
    Converting tz-aware datetime object to local tz
    Args:
        date: tz-aware datetime object
        tz:   local timezone

    Returns: local naive datetime
    """
    try:
        tz = pytz.timezone(tz)
        local_now = date.astimezone(tz).replace(tzinfo=None)
        return local_now
    except AttributeError as e:
        print '%s: (%s)' % (type(e), e)
    except UnknownTimeZoneError as e:
        print '%s: (%s)' % (type(e), e)


def convert_to_utc(date, tz):
    """
    Converting naive datetime object to utc
    Args:
        date: naive datetime object
        tz:   local timezone

    Returns: tz-aware datetime in utc
    """
    try:
        local_tz = pytz.timezone(tz)
        local_dt = local_tz.localize(date, is_dst=None)
        utc_now = local_dt.astimezone(pytz.utc)
        return utc_now
    except AttributeError as e:
        print '%s: (%s)' % (type(e), e)
    except UnknownTimeZoneError as e:
        print '%s: (%s)' % (type(e), e)


def shorten_timezone_name(local_date, tz):
    tz = pytz.timezone(tz)
    local_dt = tz.localize(local_date, is_dst=None)
    return local_dt.tzname()
