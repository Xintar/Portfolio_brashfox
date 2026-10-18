"""
Single sign-on from the React frontend (JWT) to the Django admin (session).

Flow:
1. A logged-in staff user asks the API for a short-lived ticket (JWT-authenticated).
2. The frontend POSTs the ticket to the admin-sso endpoint via a regular form.
3. The ticket is verified, a Django session is started and the user lands in /admin/.

The ticket is stateless: it is signed, valid for TICKET_MAX_AGE seconds and bound to
the user's last_login value. Django refreshes last_login when the session is created,
so a ticket can be redeemed only once, regardless of the number of server processes.
"""
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core import signing
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

TICKET_SALT = 'brashfox.admin-sso'
TICKET_MAX_AGE = 30


def _last_login_stamp(user):
    return user.last_login.timestamp() if user.last_login else 0


def make_ticket(user):
    return signing.dumps(
        {'uid': user.pk, 'stamp': _last_login_stamp(user)},
        salt=TICKET_SALT,
    )


def user_from_ticket(ticket):
    """Return the superuser a valid ticket belongs to, otherwise None."""
    try:
        payload = signing.loads(ticket, salt=TICKET_SALT, max_age=TICKET_MAX_AGE)
        user = User.objects.get(pk=payload['uid'], is_active=True, is_superuser=True)
    except (signing.BadSignature, KeyError, TypeError, User.DoesNotExist):
        return None

    if payload.get('stamp') != _last_login_stamp(user):
        return None
    return user


class AdminSsoTicketView(APIView):
    """Issue a short-lived ticket for opening the admin panel. Superusers only."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Brak dostępu do panelu administracyjnego.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response({'ticket': make_ticket(request.user)})


# The ticket itself is the secret, so the cross-origin form POST needs no CSRF token.
@csrf_exempt
def admin_sso_login(request):
    """Redeem a ticket: start a Django session and redirect to the admin."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    user = user_from_ticket(request.POST.get('ticket', ''))
    if user is None:
        return HttpResponseRedirect(reverse('admin:login'), status=303)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponseRedirect(reverse('admin:index'), status=303)
