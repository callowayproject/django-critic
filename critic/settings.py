from django.conf import settings

# The average for an instance, t
AVERAGE_TIMEOUT = getattr(settings, 'CRITIC_AVERAGE_TIMEOUT', 60)

TOTAL_TIMEOUT = getattr(settings, 'CRITIC_TOTAL_TIMEOUT', 60)

OPTIONS_TIMEOUT = getattr(settings, 'CRITIC_OPTION_CACHE_TIMEOUT', 60)

TIMEOUT = getattr(settings, 'CRITIC_TIMEOUT', 60)

CACHE_PREFIX = getattr(settings, 'CRITIC_CACHE_PREFIX', 'PRE')