# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return 'Skill %s' % self.name


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    skill = models.ForeignKey(Skill, related_name="questions")

    def __unicode__(self):
        return "Question %s for skill %s" % (self.question_text, self.skill.name)


class QuestionAnswer(models.Model):
    user = models.ForeignKey(User, related_name='selected_answers')
    question = models.ForeignKey(Question, related_name='answers_for_questions')
    answer = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Question answers"

    def __unicode__(self):
        return "Question %s answer for user %s" % (self.question.question_text, self.user)


class UserAggregatedResult(models.Model):
    user = models.ForeignKey(User, related_name='aggregated_results')
    skill = models.ForeignKey(Skill, related_name='aggregated_results')
    answer_for_self = models.CharField(max_length=20, null=True, blank=True)
    average_for_self = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "User aggregated results"

    def __unicode__(self):
        return "User %s aggregated result for skill %s" % (self.user, self.skill.name)
