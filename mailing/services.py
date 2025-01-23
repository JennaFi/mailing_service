from django.core.cache import cache

from mailing_service.settings import CACHE_ENABLED
from users.models import User
from .models import Mailing


def get_context_from_cash(user: User):
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'mailing_list'
    mailings = cache.get(f"main_page_data/{user.email}")
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
