from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView as DjangoLogOutView
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ldfinance.users.serializers import UserSerializer


class CurrentUserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class LogInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


class LogOutView(DjangoLogOutView):
    next_page = "/"
