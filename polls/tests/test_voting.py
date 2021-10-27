import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionModelTests(TestCase):
    """Model for testing Question date and time."""

    def test_can_vote(self):
        """Test that question can be vote or not."""
        time = timezone.now() + datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=60)
        question = Question(pub_date=time, end_date=future)
        self.assertIs(question.can_vote(), False)
