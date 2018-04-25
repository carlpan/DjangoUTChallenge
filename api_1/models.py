# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CallSchedule(models.Model):
    created_on = models.DateTimeField(auto_created=True)
    completed = models.BooleanField(default=False)
    confirmed_time = models.DateTimeField(null=True, blank=True,
                                          help_text='Confirmed time slot for single call schedule')

    def __unicode__(self):
        return "Call schedule %s completed %s" % (self.id, self.completed)


class CallScheduleTimeSlots(models.Model):
    call_schedule = models.ForeignKey(CallSchedule, related_name='call_schedule_time_slots')
    order = models.IntegerField(default=1, help_text="Order in which the time slot is selected")
    duration = models.IntegerField(verbose_name="Call Duration", help_text="in minutes", null=True, blank=True)
    time_slot = models.DateTimeField(null=True, blank=True, help_text='Confirmed datetime for single call')
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Call schedule time slots'

    def __unicode__(self):
        return "%s option %s time slot %s" % (self.call_schedule, self.order, self.time_slot)


class CallAppointment(models.Model):
    time_slot = models.DateTimeField()

    def __unicode__(self):
        return "Call appointment %s" % self.time_slot
