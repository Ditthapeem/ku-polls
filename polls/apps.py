"""This module is the configuration for polls app."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Configuration for polls app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
