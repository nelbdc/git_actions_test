import pytest
from django.core import mail
from unittest.mock import patch
import json
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_send_email_should_success(mailoutbox, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject="Test email send",
        message="Test",
        from_email="neldecas12@gmail.com",
        recipient_list=["njborrego@uniguajira.edu.co"],
    )

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test email send"


def test_email_without_arguments_should_send_empty_email(client):
    with patch(target="companies.views.send_mail") as mocked_send_mail_function:
        response = client.post(path=reverse("email"))
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content["status"] == "success"
        assert response_content["info"] == "email sent successfully"
        mocked_send_mail_function.assert_called_with(
            subject=None,
            message=None,
            from_email="egresados398@gmail.com",
            recipient_list=["njborrego@uniguajira.edu.co"],
        )


def test_email_with_get_methods_should_fail(client):
    response = client.get(path=reverse("email"))
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}
