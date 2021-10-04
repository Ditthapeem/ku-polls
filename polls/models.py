"""This module is create a model for Question and Choice."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """A poll question with some choices."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def is_published(self):
        """Chek that, Is question published to vote.

        Return:
            boolean
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check that, Is this question can be vote or not.

        Return:
            boolean
        """
        now = timezone.now()
        if self.end_date is not None:
            return self.is_published() and now <= self.end_date

    def __str__(self):
        """Display a text in the question.

        Parameters:
            self - the instance object
        Return:
            a string question
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )
    def was_published_recently(self):
        """Check that, Is this question was published recently or not.

        Return:
            boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """An answer to a question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Display a text in the choice.

        Parameters:
            self - the instance object
        Return:
            a string
        """
        return self.choice_text


# Create your models here.
