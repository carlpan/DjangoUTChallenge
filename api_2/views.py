# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse

from api_2.models import Question, QuestionAnswer, UserAggregatedResult

"""
Imagine a user is doing some assessment that contains 5 questions. Each question is
related to a skill and the answer is value between 0-100. The api below takes in
user's answers and save them, in addition, it dispatches a method to gather each answer
and calculates average answer for the user.
Please refer to admin page to see some existing data to get a sense of what the api does.
"""


@csrf_exempt
def save_assessment(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    user = request.user
    if request.method == 'POST':
        response = json.loads(request.body)

        answers_count = 0
        for k, v in response.iteritems():
            try:
                question = Question.objects.get(pk=int(k))
                answer = v.get("answer", None)
                QuestionAnswer.objects.create(
                    user=user,
                    question=question,
                    answer=answer
                )
                answers_count += 1
            except (ObjectDoesNotExist, ValueError):
                pass
        if answers_count >= 5:
            calculate_aggregated_result_for_user(user)
            return HttpResponse("Saved successfully")
        else:
            user.selected_answers.all().delete()
            return HttpResponseBadRequest("Error in saving answers")


def calculate_aggregated_result_for_user(user):
    """
    This method takes user answers and save it to a new table
    with each answer and the average of all answers.
    In reality, a more robust calculations are done to user's inputs.
    This process usually runs asynchronously via a background job.
    """
    for answer in user.selected_answers.all():
        # Create aggregated_result instance for each question answer
        aggregated_result, created = UserAggregatedResult.objects.\
            get_or_create(user=user, skill=answer.question.skill)
        # Set each answer
        aggregated_result.answer_for_self = answer.answer
        # Calculate and set average for all question answers
        average_for_self = calculate_average_for_skills(user)
        aggregated_result.average_for_self = average_for_self
        # Save
        aggregated_result.save()


def calculate_average_for_skills(user):
    """
    Calculate average value over all answers.
    """
    answer_total = 0
    valid_answer_count = 0
    for answer in user.selected_answers.all():
        try:
            answer = int(answer.answer)
            answer_total += answer
            valid_answer_count += 1
        except ValueError:
            pass
    return int(float(answer_total / valid_answer_count))
