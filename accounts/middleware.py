import time
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class KeycloakOIDCMiddleware(MiddlewareMixin):
    """Middleware to attach Keycloak OIDC session user to Django request.

    Notes:
    - Only active if `USE_KEYCLOAK` is True.
    - Uses token expiry compared to `time.time()`.
    - Does not re-login an already authenticated user.
    - Fails safely (leaves `request.user` untouched) if token invalid.
    """

    def process_request(self, request):
        if not getattr(settings, 'USE_KEYCLOAK', False):
            return None

        token = request.session.get('access_token')
        if not token:
            return None

        # If the user is already authenticated, only refresh fields if necessary
        try:
            payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
        except Exception:
            # Invalid token; clear session and skip
            request.session.pop('access_token', None)
            return None

        exp = payload.get('exp')
        if exp and exp < time.time():
            # Token expired
            request.session.flush()
            return redirect('login')

        username = payload.get('preferred_username') or payload.get('sub')
        if not username:
            return None

        try:
            user, created = User.objects.get_or_create(username=username)
            # Update user fields from token claims (safe defaults)
            user.email = payload.get('email', user.email or '')
            # custom claims may be in 'realm_access' or direct claim names; guard access
            user.role = payload.get('role', getattr(user, 'role', 'EMPLOYEE'))
            user.department = payload.get('department', getattr(user, 'department', 'DIGITAL'))
            user.keycloak_id = payload.get('sub', getattr(user, 'keycloak_id', ''))
            user.save()

            # Log in user if not already authenticated
            if not request.user.is_authenticated:
                login(request, user)
                request.user = user
        except Exception:
            # On any DB error, leave request.user as-is and allow other auth backends
            request.user = getattr(request, 'user', AnonymousUser())

        return None
