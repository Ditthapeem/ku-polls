"""This module handle the request and generate each template."""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice, Vote
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm



def index(request):
    """Display the index page.

    Parameters:
            request - an HttpRequest containing the client's request data
    Return:
        an HttpResponse
    """
    latest_question_list = Question.objects.\
        filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    """Display the detail page.

    Parameters:
            request - an HttpRequest containing the client's request data
            question_id - an id of each question
    Return:
        an HttpResponse
    """
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote() and question.is_published():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        messages.error(request, "Question is not available.")
        return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """A result page."""

    model = Question
    template_name = 'polls/results.html'

@login_required(login_url='/accounts/login/')
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
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        user = request.user
        vote = get_vote_for_user(question, user)
        if not vote:
            vote = Vote(user=user, choice=selected_choice)
        else:
            vote.choice = selected_choice
        vote.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))

def get_vote_for_user(question, user):
    """
    Find and return an existing vote for user on poll question.

    Returns:
        The user vote
    """
    try:
        vote = Vote.objects.filter(user=user).filter(choice__question=question)
        if vote.count() == 0:
            return None
        else:
            return vote[0]
    except Vote.DoesNotExist:
        return None

# def signup(request):
#     """Register a new user."""
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_passwd = form.cleaned_data.get('password')
#             user = authenticate(username=username,
#                                 password=raw_passwd)
#             login(request, user)
#             return redirect('polls')
#         # what if form is not valid?
#         # we should display a message in signup.html
#     else:
#         form = UserCreationForm()
#     return render(request,
#                   'registration/signup.html',
#                   {'form':form})
