from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from api_1.models import CallSchedule, CallAppointment


@receiver(pre_save, sender=CallSchedule, dispatch_uid="create_call_appointment_on_call_schedule_accept")
def create_call_appointment_on_call_schedule_accept(sender, instance, **kwargs):
    """
    Signal handler to create a new call appointment entry upon accepting call schedule.

    :param sender:      sender CallSchedule
    :param instance:    CallSchedule instance to be saved
    :param kwargs:      kwargs
    """
    try:
        obj = sender.objects.get(pk=instance.pk)
        if obj.completed != instance.completed:
            if instance.completed:
                CallAppointment.objects.create(
                    time_slot=instance.confirmed_time
                )
    except ObjectDoesNotExist:
        pass
