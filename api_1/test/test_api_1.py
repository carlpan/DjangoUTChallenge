from datetime import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from freezegun import freeze_time

from api_1.models import *

class API1TestCase(TestCase):
    def setUp(self):
        """
        OPTIONAL
        if you think you need to prepare some universal data for
        each test case to use, then do it here.
        """
        self.client.post(reverse("conference_call_schedules"), {
            "duration1": 30,
            "datetime1": "04/28/2017 12:30",
            "duration2": 30,
            "datetime2": "04/28/2017 12:30",
            "duration3": 30,
            "datetime3": "04/28/2017 13:30"
        })
        pass

    @freeze_time("2018-04-01")
    def test_create_call_schedules_success(self):
        
        """This is an example test case.
        YOU SHOULD CONTINUE ADDING MORE TESTS TO COMPLETE THIS TEST CASE."""
        response = self.client.post(reverse("conference_call_schedules"), {
            "duration1": 30,
            "datetime1": "04/28/2017 12:30",
            "duration2": 30,
            "datetime2": "04/28/2017 12:30",
            "duration3": 30,
            "datetime3": "04/28/2017 13:30"
        })
        
        self.assertEqual(response.status_code, 200)
        # CONTINUE BELOW

    """
    Write rest of the tests belowls
    Some points for testing are:
    - test on create call schedule fail
    - test on /call_schedules/ GET returns correct template
    - test expected behavior or accepting/remove a time slot
    - test relevant cases for adding a new time slot
    """

    def test_call_schedules_get_success(self):
        
        response = self.client.get(reverse("conference_call_schedules"))
        
        self.assertEqual(response.status_code, 200)

    def test_remove_time_slot_success(self):

        response = self.client.post(reverse("accept_remove_time_slot"), {
            "identifier":1,
            "order":3,
            "for_accept":0
        })
        
        self.assertEqual(response.status_code, 200)

    def test_accept_time_slot_success(self):
        
        response = self.client.post(reverse("accept_remove_time_slot"), {
            "identifier":1,
            "order":3,
            "for_accept":1
        })
        
        self.assertEqual(response.status_code, 200)

    def test_add_single_time_slot_success(self):

        self.client.post(reverse("accept_remove_time_slot"), {
            "identifier":1,
            "order":3,
            "for_accept":0
        })

        response = self.client.post(reverse("add_single_time_slot"), {
            "duration1":40,
            "datetime1":"04/28/2017 14:30",
            "identifier":1
        })

        self.assertEqual(response.status_code, 200)