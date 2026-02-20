# ISO 9001 Intelligent Document Management and Compliance Evaluation System

## Features
- Keycloak OIDC authentication with fallback to local Django auth
- Role-based dashboards (ADMIN, TEAMLEAD, EMPLOYEE)
- Department-based access control
- Document management (PDF/DOCX upload, status workflow)
- Simulated AI analysis (PyPDF2, compliance scoring)
- PDF audit reporting (reportlab)
- Bootstrap 5 modern UI
- PostgreSQL database

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure PostgreSQL and Keycloak settings in `settings.py` or environment variables.
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```

## Keycloak Client Example
See `iso9001-client.json` for a sample Keycloak client configuration. You can import this JSON directly into the Keycloak admin console (Realm: `iso9001-realm`) as a client to create `iso9001-client` quickly. After import, ensure the redirect URI `http://127.0.0.1:8000/accounts/callback/` is present in the client's Redirect URIs.

## Running Keycloak locally (avoid Jenkins on 8080)

If you have Jenkins running on port 8080, start Keycloak on a different host port (8081) and point Django to it.

1. Start Keycloak (Docker) on port 8081:
```powershell
docker run -p 8081:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:21.1.0 start-dev
```

2. Update environment and run Django (PowerShell):
```powershell
$env:KEYCLOAK_SERVER_URL = "http://127.0.0.1:8081"
$env:USE_KEYCLOAK = "true"
python manage.py runserver
```

3. In Keycloak admin, configure the `iso9001-client` client redirect URI:
```
http://127.0.0.1:8000/accounts/callback/
```

If you prefer to run Keycloak on port 8080, stop Jenkins first (requires admin) or change the port mapping for Jenkins.

## Production
- Set `DEBUG = False` and configure allowed hosts
- Use secure cookies and CSRF protection
- Use Gunicorn/UWSGI for deployment
- Configure HTTPS
