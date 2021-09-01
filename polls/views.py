from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Question


# Create your views here.


def index(request):
    """Display an index for this app.

    Parameters:
            request - an HttpRequest containing the client's request data
    Return:
        an HttpResponse
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list':latest_question_list,

    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Display an index of that question.

    Parameters:
            request - an HttpRequest containing the client's request data
            question_id - an id of each question
    Return:
        an HttpResponse
    """
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    """Display an index of the result of that question.

    Parameters:
            request - an HttpRequest containing the client's request data
            question_id - an id of each question
    Return:
        an HttpResponse
    """
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """Display an index of question that you voted.

    Parameters:
            request - an HttpRequest containing the client's request data
            question_id - an id of each question
    Return:
        an HttpResponse
    """
    return HttpResponse("You're voting on question %s." % question_id)


def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
