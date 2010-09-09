"""
django-critic settings.
"""

from django.conf import settings

# Holds the rating definitions.
RATING_METHODS = getattr(settings, 'CRITIC_RATING_METHODS', [])

# True|False, to allow a user to change their rating.
ALLOW_CHANGE = getattr(settings, 'CRITIC_ALLOW_CHANGE', False)

# This is the name of the attribute that will be added to the models.
RATING_ATTR = getattr(settings, 'CRITIC_RATING_ATTRIBUTE', 'ratings')