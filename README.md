LeadTracker — Back-end (Django REST) 🐍
Short description

Django REST API that powers LeadTracker: user auth (JWT), freelancer profiles, SerpApi Google Maps searches, lead persistence, and call tracking.
Tech stack

Python, Django, Django REST Framework, rest_framework_simplejwt, SerpApi (Google Maps). (Dev DB: SQLite; change to Postgres in production.)
Key models

Freelancer — profile linked to User
Lead — business lead (name, phone, email, website, address, rating)
CallStatus — boolean or status for calls (called / not called)
Requirements

Python 3.10+ (recommended)
pipenv or pip
SerpApi account + API key (for Google Maps results)
Quick local setup

Environment variables (examples)

SECRET_KEY — Django secret key (required for production)
DEBUG — True/False
ALLOWED_HOSTS — host list for production
MAP_API_KEY — SerpApi API key (required for business search)
Set these in .env or your Docker environment. The app reads settings.MAP_API_KEY.
Docker (optional)

A Dockerfile and docker-compose.yml exist in map. Use them to run the API in containers:
API endpoints (examples)

Register: POST /create-user/ — { "username": "...", "email": "...", "password": "..." }
Response includes token and refresh.
JWT token: POST /api/token/ — { "username", "password" }
Create freelancer/profile: POST /freelancer-details/ — { "skills": "..." } (auth required)
Search businesses (SerpApi): POST /get-business-details/ — { "business": "...", "location": "..." } (auth + freelancer profile required)
List leads: GET /list-leads/ (auth required)
Toggle / update call status: GET or POST /update-call-status/<lead_id>/ (auth required) — POST payload { "called": true }
Delete lead: DELETE /delete-lead/<pk>/ (auth required)
Note: exact path names are in views.py. Adjust frontend accordingly if you rename routes.

Sample curl flow

SerpApi & Usage

Create an account at https://serpapi.com/, copy your API key, and set MAP_API_KEY in Django settings or .env.
Be mindful of usage limits and billing.
Testing

Logging & debugging

The get_bussines_details view prints debugging info to console when SerpApi responses are unexpected — helpful for troubleshooting returned payloads and keys.
Production notes

Replace SQLite with PostgreSQL for production.
Use environment variables for SECRET_KEY and MAP_API_KEY.
Use HTTPS, configure ALLOWED_HOSTS and proper CORS if front-end is hosted separately.
Contributing

Fork → feature branch → open a PR. Run tests and linters before proposing changes.
License

MIT (or choose an appropriate license)
