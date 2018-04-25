import json
import uuid
import random

from django.test import TestCase
from django.core.urlresolvers import reverse

from api_2.models import *


class API2TestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(username="api_2_user", password="test123")
        # Create skill and question
        for skill in range(0, 5):
            skill_obj = Skill.objects.create(name=str(uuid.uuid4())[:10])
            Question.objects.create(question_text=str(uuid.uuid4()), skill=skill_obj)

    def question_answer_request_body_1(self):
        """
        This is an example method to build answers request body for POST.
        """
        request_body = dict()
        for question in Question.objects.all():
            request_body[int(question.pk)] = {
                "answer": random.randint(0, 100)
            }
        return request_body

    """
    Write your tests below
    Some points for testing are:
    - test submit answers success (5 answers) 
    - test submit answers fail (auth failure)
    - test submit answers fail (< 5 answers)
    - test expected behavior of generating aggregated result
    """
