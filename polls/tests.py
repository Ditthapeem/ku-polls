from django.test import TestCase
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.


class QuestionModelTests(TestCase):
    """Model for testing Question date and time"""

    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() returns False for questions whose pub_date
            is in the future.

        Return:
            an boolean
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=31)
        future_question = Question(pub_date=time, end_date=future)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() returns False for questions whose pub_date
            is older than 1 day.

        Return:
            an boolean
        """
        future = timezone.now() + datetime.timedelta(days=30)
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time, end_date=future)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() returns True for questions whose pub_date
            is within the last day.

        Return:
            an boolean
        """
        future = timezone.now() + datetime.timedelta(days=30)
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=future)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=time, end_date=future)
        self.assertIs(question.is_published(), True)

    def test_can_vote(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=60)
        question = Question(pub_date=time, end_date=future)
        self.assertIs(question.can_vote(), False)


def create_question(question_text, days, date_future):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    future = timezone.now() + datetime.timedelta(days=date_future)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=future)


class QuestionIndexViewTests(TestCase):
    """Test for question index view"""

    def test_no_question(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30, date_future=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30, date_future=60)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30, date_future=-15)
        create_question(question_text="Future question.", days=30, date_future=32)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30, date_future=-15)
        question2 = create_question(question_text="Past question 2.", days=-5, date_future=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1],)


class QuestionDetailViewTests(TestCase):
    """Test for detail question."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5, date_future=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5, date_future=-2)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
