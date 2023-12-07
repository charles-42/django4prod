import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_connexion():
    first_object = User.objects.first
    assert first_object is not None