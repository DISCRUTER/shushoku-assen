import pytest

from tests.factories import unique_suffix


RESOURCES = [
    "/api/v1/utils/roles",
    "/api/v1/utils/branch",
    "/api/v1/utils/academic-degree",
    "/api/v1/utils/industry",
    "/api/v1/utils/skills",
]


def payload_for(resource):
    name = f"{resource.rsplit('/', 1)[-1]}-{unique_suffix()}"
    return {"name": name, "description": f"Test entry {name}"}


@pytest.mark.parametrize("resource", RESOURCES)
def test_get_is_public(unauthenticated_client, resource):
    response = unauthenticated_client.get(resource)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


@pytest.mark.parametrize("resource", RESOURCES)
def test_get_returns_seeded_lookups(unauthenticated_client, resource):
    response = unauthenticated_client.get(resource)
    names = [entry["name"] for entry in response.get_json()]
    assert len(names) >= 2


@pytest.mark.parametrize("resource", RESOURCES)
def test_post_admin_creates_entry(admin_client, resource):
    payload = payload_for(resource)
    response = admin_client.post(resource, json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["name"] == payload["name"]
    assert body["id"]

    listed = admin_client.get(resource)
    assert payload["name"] in [entry["name"] for entry in listed.get_json()]


@pytest.mark.parametrize("resource", RESOURCES)
def test_post_unauthenticated_rejected(unauthenticated_client, resource):
    response = unauthenticated_client.post(resource, json=payload_for(resource))
    assert response.status_code == 401


@pytest.mark.parametrize("resource", RESOURCES)
def test_post_student_forbidden(student_client, resource):
    response = student_client.post(resource, json=payload_for(resource))
    assert response.status_code == 403
    assert response.get_json()["msg"] == "Access forbidden: Insufficient permissions"


@pytest.mark.parametrize("resource", RESOURCES)
def test_post_company_forbidden(approved_company_client, resource):
    response = approved_company_client.post(resource, json=payload_for(resource))
    assert response.status_code == 403


def test_post_missing_name_unprocessable(admin_client):
    response = admin_client.post("/api/v1/utils/roles", json={"description": "no name"})
    assert response.status_code == 422


def test_post_duplicate_name_conflict_surfaces_as_server_error(admin_client):
    from tests.factories import get_or_create_role

    existing = get_or_create_role("Admin")
    response = admin_client.post(
        "/api/v1/utils/roles", json={"name": existing.name, "description": "dup"}
    )
    assert response.status_code == 500


def test_post_duplicate_branch_name_surfaces_as_server_error(admin_client):
    from tests.factories import get_or_create_branch

    existing = get_or_create_branch()
    response = admin_client.post("/api/v1/utils/branch", json={"name": existing.name})
    assert response.status_code == 500
