
from django.contrib.auth.backends import ModelBackend

from funcy import first

from apps.users.services import verify_telegram_authentication
from apps.users.models import User



class AuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
            verify_telegram_authentication(request.data)
            if id := request.data.get("id"):
                return first(User.objects.get_or_create(telegram_id=id))
