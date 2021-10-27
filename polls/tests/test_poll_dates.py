import datetime
from django.test import TestCase
from django.utils import timezone

from polls.models import Question



class QuestionModelTests(TestCase):
    """Model for testing Question date and time."""

    def test_was_published_recently_with_future_question(self):
        """Check questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=31)
        future_question = Question(pub_date=time, end_date=future)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Check questions whose pub_date is older than 1 day."""
        future = timezone.now() + datetime.timedelta(days=30)
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time, end_date=future)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Check questions whose pub_date is within the last day."""
        now = timezone.now()
        future = now + datetime.timedelta(days=30)
        time = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=future)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published(self):
        """Test that question are publish or not."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=time, end_date=future)
        self.assertIs(question.is_published(), True)

    def test_can_vote(self):
        """Test that question can be vote or not."""
        time = timezone.now() + datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=60)
        question = Question(pub_date=time, end_date=future)
        self.assertIs(question.can_vote(), False)
