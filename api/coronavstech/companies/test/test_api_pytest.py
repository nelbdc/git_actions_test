import pytest
import json
from django.urls import reverse
# from companies.models import Company
from companies.models import Company

company_url = reverse("companies-list")
pytestmark = pytest.mark.django_db  # module declaration for marks in pytest


## -------------- Test get companies -------------- ##


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(company_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.fixture
def amazon():
    return Company.objects.create(name="amazon")


def test_one_companies_exist_should_return_succeed(client, amazon) -> None:
    response = client.get(company_url)
    response_content = json.loads(response.content)[0]
    assert response_content.get("name") == amazon.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


## -------------- Test post companies -------------- ##


def test_create_company_without_argument_should_faild(client) -> None:
    response = client.post(path=company_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_faild(client) -> None:
    test_company = Company.objects.create(name="Amazon")

    response = client.post(path=company_url, data={"name": "Amazon"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_should_be_default(client) -> None:
    response = client.post(path=company_url, data={"name": "Amazon"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=company_url, data={"name": "Amazon", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"


def test_create_conpany_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=company_url, data={"name": "Amazon", "status": "Wrongstatus"}
    )
    assert response.status_code == 400
    assert "Wrongstatus" in str(response.content)


# -------------- learn about fixture test ----------------- #


@pytest.fixture
def create_company_fixture(companies):
    return Company.objects.bulk_create([Company(name=x) for x in companies])


@pytest.mark.parametrize("companies", [("Twitch", "Tiktok", "Test Company INC")])
def test_multiple_companies_exist_should_succed(client, create_company_fixture) -> None:
    companies_names = set(map(lambda x: x.name, create_company_fixture))
    response_content = client.get(company_url).json()
    assert len(response_content) == len(companies_names)
    response_companies_names = set(map(lambda x: x.get("name"), response_content))
    response_companies_names == companies_names


@pytest.fixture
def company(**kwargs):
    def _company_factory(**kwargs):
        company_name = kwargs.pop("name", "Test Company INC")
        return Company.objects.create(name=company_name)

    return _company_factory


def test_multiple_companies_exist_should_succed_2(client, company) -> None:
    twitch = company(name="Twitch")
    tiktok = company(name="Tiktok")
    test_company = company(name="Test Company INC")
    response_content = client.get(company_url).json()
    companies_names = {twitch.name, tiktok.name, test_company.name}
    assert len(response_content) == len(companies_names)
    response_companies_names = set(map(lambda x: x.get("name"), response_content))
    response_companies_names == companies_names


@pytest.fixture
def companies(request, company):
    companies = []
    names = request.param  # receive arguments passed a this function
    for i in names:
        companies.append(company(name=i))
    return companies


@pytest.mark.parametrize(
    "companies",
    [["Twitch", "Tiktok", "Test Company INC"], ["Facebook", "Instagram"]], # arguments passed
    ids=["3 companies", "Mark companies"],  # pass a name for the test
    indirect=True,
)
def test_multiple_companies_exist_should_succed_3(client, companies) -> None:
    companies_names = set(map(lambda x: x.name, companies))
    response_content = client.get(company_url).json()
    assert len(response_content) == len(companies_names)
    response_companies_names = set(map(lambda x: x.get("name"), response_content))
    response_companies_names == companies_names
