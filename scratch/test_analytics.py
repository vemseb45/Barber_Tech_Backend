import os
import django
import sys

# Setup django
sys.path.append('e:/Xampp/htdocs/BarberTech/Barber_Tech_Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from agenda.views_analytics import AdminAnalyticsView
from rest_framework.test import APIRequestFactory, force_authenticate
from usuarios.models import Usuario

factory = APIRequestFactory()
user = Usuario.objects.filter(rol='Admin').first()

if not user:
    print("No admin user found")
    sys.exit(1)

request = factory.get('/api/agenda/analytics/', {'timeRange': 'Últimos 30 días'})
force_authenticate(request, user=user)
view = AdminAnalyticsView.as_view()

try:
    response = view(request)
    print("Response status:", response.status_code)
    print("Response data:", response.data)
except Exception as e:
    import traceback
    print("Error detected:")
    traceback.print_exc()
