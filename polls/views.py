import math

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.forms import HypotenuseFrom, MyPersonModelForm, ReminderForm

from .models import Choice, MyPerson, Question
from .tasks import send_date_reminder

class IndexView(generic.ListView):
    template_name = '../templates/polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]