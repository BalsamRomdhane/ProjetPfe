import requests
import logging
from urllib.parse import urlencode
import os
import base64
import hashlib
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LocalLoginForm
from django.http import HttpResponse
import jwt

# Keycloak endpoints
KC_AUTH_URL = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth"
KC_TOKEN_URL = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
KC_LOGOUT_URL = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout"


logger = logging.getLogger(__name__)


def login_view(request):
    if settings.USE_KEYCLOAK:
        redirect_uri = settings.KEYCLOAK_REDIRECT_URI
        # Build auth URL with PKCE (S256) to satisfy Keycloak client settings
        # Generate a high-entropy code_verifier, store it in the session and send the code_challenge
        code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
        request.session['pkce_code_verifier'] = code_verifier

        # Build auth URL with proper URL-encoding to avoid malformed redirect_uri
        params = {
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'response_type': 'code',
            'scope': 'openid profile email',
            'redirect_uri': redirect_uri,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        }
        auth_url = f"{KC_AUTH_URL}?{urlencode(params)}"
        logger.debug('Keycloak auth_url: %s', auth_url)
        return render(request, 'accounts/login.html', {'auth_url': auth_url, 'use_keycloak': True})
    else:
        if request.method == 'POST':
            form = LocalLoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('post_login')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            form = LocalLoginForm()
        return render(request, 'accounts/login.html', {'form': form, 'use_keycloak': False})

def oidc_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('login')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.KEYCLOAK_REDIRECT_URI,
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
    }
    # If we previously generated a PKCE verifier, include it in the token exchange
    code_verifier = request.session.pop('pkce_code_verifier', None)
    if code_verifier:
        data['code_verifier'] = code_verifier
    resp = requests.post(KC_TOKEN_URL, data=data)
    if resp.status_code == 200:
        token_data = resp.json()
        access_token = token_data['access_token']
        id_token = token_data.get('id_token')
        request.session['access_token'] = access_token
        payload = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["RS256"])
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, created = User.objects.get_or_create(username=payload['preferred_username'])
        user.email = payload.get('email', '')
        user.role = payload.get('role', 'EMPLOYEE')
        user.department = payload.get('department', 'DIGITAL')
        user.keycloak_id = payload.get('sub', '')
        user.save()
        login(request, user)
        return redirect('post_login')
    else:
        messages.error(request, 'OIDC authentication failed.')
        return redirect('login')

def logout_view(request):
    if settings.USE_KEYCLOAK:
        token = request.session.get('access_token')
        request.session.flush()
        logout(request)
        logout_url = f"{KC_LOGOUT_URL}?post_logout_redirect_uri={settings.KEYCLOAK_LOGOUT_REDIRECT_URI}&client_id={settings.KEYCLOAK_CLIENT_ID}"
        return redirect(logout_url)
    else:
        logout(request)
        return render(request, 'accounts/logout.html')

def unauthorized_view(request):
    return render(request, 'accounts/unauthorized.html')

@login_required
def post_login_redirect(request):
    role = getattr(request.user, 'role', 'EMPLOYEE')
    if role == 'ADMIN':
        return redirect('/admin-dashboard/')
    elif role == 'TEAMLEAD':
        return redirect('/department-dashboard/')
    else:
        return redirect('/employee-dashboard/')
