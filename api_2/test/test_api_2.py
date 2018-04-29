import json
import uuid
import random

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from api_2.models import *


class API2TestCase(TestCase):
    def setUp(self):
        # Create user
        # self.user = User.objects.create(username="api_2_user", password="test123")
        user = User.objects.create(username='api_2_user')
        user.set_password('test123')
        user.save()

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

    def question_answer_request_body_2(self):
        """
        Create request body with one answer
        """
        request_body = dict()
        skill_obj = Skill.objects.create(name=str(uuid.uuid4())[:10])
        question = Question.objects.create(question_text=str(uuid.uuid4()), skill=skill_obj)
        request_body[int(question.pk)] = {
            "answer": random.randint(0, 100)
        }
        return request_body

    def test_save_assessment(self):
        self.client = Client()
        login = self.client.login(username='api_2_user', password='test123')

        # make sure client is login.
        self.assertTrue(login)

        request_body = self.question_answer_request_body_1()
        response = self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")

        # test if save_assessment is successful
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Saved successfully")

        # if the answers are less than 5, it should return 400
        request_body = self.question_answer_request_body_2()
        response = self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")

        # test if save_assessment is successful
        self.assertEquals(response.status_code, 400)



    """
    Write your tests below
    Some points for testing are:
    - test submit answers success (5 answers)
    - test submit answers fail (auth failure)
    - test submit answers fail (< 5 answers)
    - test expected behavior of generating aggregated result
    """
