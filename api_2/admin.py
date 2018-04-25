# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api_2.models import Skill, Question, QuestionAnswer, UserAggregatedResult


class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "skill",)
    list_filter = ("skill",)


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "user", "answer",)
    list_filter = ("user",)


class UserAggregatedResultAdmin(admin.ModelAdmin):
    list_display = ("id", "skill", "user", "answer_for_self", "average_for_self",)
    list_filter = ("skill", "user",)


admin.site.register(Skill, SkillAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(UserAggregatedResult, UserAggregatedResultAdmin)

