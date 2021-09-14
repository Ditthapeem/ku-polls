from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone
from django.contrib import messages

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote() and question.is_published():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        messages.error(request, "Question is not available.")
        return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """A result page"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Redisplay the question voting form.

    Parameters:
            request - an HttpRequest containing the client's request data
            question_id - an id of each question
    Return:
        an HttpResponse
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



