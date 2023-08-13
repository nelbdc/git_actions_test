import json
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse
from companies.models import Company


@pytest.mark.django_db
class BasicCompaniesTestConfig(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_url = reverse("companies-list")

    def tearDown(self):
        pass


class TestGetCompanies(BasicCompaniesTestConfig):
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.company_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_onae_companies_exist_should_return_succeed(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.company_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        test_company.delete()


class TestPostCompanies(BasicCompaniesTestConfig):
    def test_create_company_without_argument_should_faild(self) -> None:
        response = self.client.post(path=self.company_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_faild(self) -> None:
        test_company = Company.objects.create(name="Amazon")

        response = self.client.post(path=self.company_url, data={"name": "Amazon"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_should_be_default(self) -> None:
        response = self.client.post(path=self.company_url, data={"name": "Amazon"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            path=self.company_url, data={"name": "Amazon", "status": "Layoffs"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_conpany_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.company_url, data={"name": "Amazon", "status": "Wrongstatus"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrongstatus", str(response.content))

    @pytest.mark.xfail
    def test_should_to_ok_if_fails(self):
        self.assertEqual(2, 3)

    @pytest.mark.skip
    def test_should_skipped(self):
        self.assertEqual(1, 2)


def raise_covid19_exception():
    raise ValueError("Coronavirus Exception")


def test_raise_covid19_exepction_should_fail():
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "Coronavirus Exception" == str(e.value)


import logging

logger = logging.getLogger("logs")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()

    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logging.info("I am loggin info level")
        assert "I am loggin info level" in caplog.text
