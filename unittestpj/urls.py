"""unittestpj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from api_1 import views as api_1_views
from api_2 import views as api_2_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^call_schedules/$', api_1_views.conference_call_schedules, name='conference_call_schedules'),
    url(r'^accept-remove-time-slot/$', api_1_views.accept_remove_time_slot, name='accept_remove_time_slot'),
    url(r'^add-single-time-slot/$', api_1_views.add_single_time_slot, name='add_single_time_slot'),
    url(r'^save-assessment/$', api_2_views.save_assessment, name='save_assessment',)
]
