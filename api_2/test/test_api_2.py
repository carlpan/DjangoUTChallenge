import json
import uuid
import random
from api_2.views import *

from django.test import TestCase
from django.core.urlresolvers import reverse

from api_2.models import *
from django.contrib.auth import authenticate as auth
from django.contrib.auth import login
class API2TestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username="api_2_user", password="test123")
        self.user = auth(self, username="api_2_user", password="test123")
        self.user.set_password("test123")
        self.user.save()
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

    def test_submit_answer_success(self):
        
        request_body = dict()
        for question in Question.objects.all():
            request_body[int(question.pk)] = {
                "answer": random.randint(0, 100)
            }
        self.client.login(username="api_2_user",password="test123")
        response = self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")
        
        self.assertEquals(response.status_code, 200)
    
    def test_submit_answer_fail_auth_failure(self):
        
        request_body = dict()
        for question in Question.objects.all():
            request_body[int(question.pk)] = {
                "answer": random.randint(0, 100)
            }
        response = self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")
        
        self.assertEquals(response.status_code, 401)

    def test_submit_answer_fail_less_than_5(self):
        request_body = {}
        for question in Question.objects.all():
            request_body[int(question.pk)] = {
                "answer": random.randint(0, 100)
            }
        request_body.popitem()
        self.client.login(username="api_2_user",password="test123")
        response = self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")
        
        self.assertEquals(response.status_code, 400)

    def test_calculated_aggregrate_result_for_user(self):
        request_body = {}
        for question in Question.objects.all():
            request_body[int(question.pk)] = {
                "answer": random.randint(0, 100)
            }
        answer_total = 0
        for k, v in request_body.iteritems():
            answer_total += v.get("answer")

        answer_total = answer_total/5

        self.client.login(username="api_2_user",password="test123")
        self.client.post(reverse("save_assessment"), json.dumps(request_body), content_type="application/json")
        value = calculate_average_for_skills(self.user)
        
        self.assertEquals(value, answer_total)