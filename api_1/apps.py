# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class Api1Config(AppConfig):
    name = 'api_1'

    def ready(self):
        import api_1.signals
