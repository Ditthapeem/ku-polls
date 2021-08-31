import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    """A poll question with some choices."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """Display a text in the question

        Parameters:
            self - the instance object
        Return:
            a string question
        """
        return self.question_text

    def was_published_recently(self):
        """Check that, Is this question was published recently.

        Parameters:
            self - the instance object
        Return:
            boolean
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    """An answer to a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Display a text in the choice

        Parameters:
            self - the instance object
        Return:
            a string
        """
        return self.choice_text


# Create your models here.
