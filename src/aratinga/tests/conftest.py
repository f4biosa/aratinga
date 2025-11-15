# aratinga/src/aratinga/tests/conftest.py

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def admin_user():
    """
    Cria ou atualiza o superusuário de teste PADRÃO ('adminTester')
    garantindo que a senha esteja CORRETAMENTE criptografada,
    conforme definido em test_theme.py.
    """
    User = get_user_model()

    # Seus dados de teste corretos
    username = "adminTester"
    password = "Admin.Tester@001"

    # Busca ou cria o usuário
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": "admintester@example.com"}
    )

    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return user