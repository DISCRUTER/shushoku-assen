import pytest

from application.util_enum import ApplicationStatus, DriveStatus, JobType

from tests.factories import (
    get_or_create_branch,
    get_or_create_degree,
    get_or_create_industry,
    make_application,
    make_company,
    make_drive,
    make_placement,
    make_student,
)


def snapshot(admin_client, endpoint, query=None):
    response = admin_client.get(endpoint, query_string=query or {})
    assert response.status_code == 200
    return response.get_json()["data"]


def as_count_map(data):
    return {row[0]: row[1] for row in data}


def merged(baseline, deltas):
    combined = dict(baseline)
    for key, value in deltas.items():
        combined[key] = combined.get(key, 0) + value
    return combined


def sorted_counts(data):
    return sorted(row[1] for row in data)


STUDENTS = "/api/v1/analytics/students"
COMPANY = "/api/v1/analytics/company"
DRIVES = "/api/v1/analytics/drives"
APPLICATION = "/api/v1/analytics/application"
PLACEMENTS = "/api/v1/analytics/placements"


@pytest.fixture()
def dataset(app, admin_client):
    baselines = {
        "students_by_branch": as_count_map(snapshot(admin_client, STUDENTS)),
        "students_total": snapshot(admin_client, STUDENTS, {"all": "true"})[0][1],
        "students_by_degree": as_count_map(snapshot(admin_client, STUDENTS, {"academic_degree": "true"})),
        "company_by_industry": as_count_map(snapshot(admin_client, COMPANY)),
        "company_total": snapshot(admin_client, COMPANY, {"all": "true"})[0][1],
        "drives_by_job_type": sorted_counts(snapshot(admin_client, DRIVES)),
        "drives_total": snapshot(admin_client, DRIVES, {"all": "true"})[0][1],
        "application_total": snapshot(admin_client, APPLICATION, {"all": "true"})[0][1],
        "placements_total": snapshot(admin_client, PLACEMENTS, {"all": "true"})[0][1],
        "placements_by_company": as_count_map(snapshot(admin_client, PLACEMENTS)),
    }

    cs = get_or_create_branch("Computer Science")
    me = get_or_create_branch("Mechanical Engineering")
    btech = get_or_create_degree("B.Tech")
    mtech = get_or_create_degree("M.Tech")
    it = get_or_create_industry("Information Technology")
    fin = get_or_create_industry("Finance")

    s1 = make_student(branch=cs, academic_degree=btech)
    s2 = make_student(branch=cs, academic_degree=btech)
    s3 = make_student(branch=cs, academic_degree=mtech)
    s4 = make_student(branch=me, academic_degree=btech)

    c1 = make_company(industry=it)
    c2 = make_company(industry=it)
    c3 = make_company(industry=fin)

    d1 = make_drive(c1, status=DriveStatus.OPEN, job_type=JobType.INTERNSHIP)
    d2 = make_drive(c1, status=DriveStatus.CLOSED, job_type=JobType.FULL_TIME)
    d3 = make_drive(c2, status=DriveStatus.PENDING, job_type=JobType.FULL_TIME)
    d4 = make_drive(c3, status=DriveStatus.OPEN, job_type=JobType.PART_TIME)

    a1 = make_application(s1, d1)
    a2 = make_application(s2, d1)
    a3 = make_application(s1, d2, status=ApplicationStatus.SHORTLISTED)

    p1 = make_placement(s1, c1, d1)
    p2 = make_placement(s2, c1, d1)
    p3 = make_placement(s3, c2, d3)

    return {
        "baselines": baselines,
        "students": [s1, s2, s3, s4],
        "companies": [c1, c2, c3],
        "drives": [d1, d2, d3, d4],
        "applications": [a1, a2, a3],
        "placements": [p1, p2, p3],
    }


def test_students_analytics_grouped_by_branch(student_client, dataset):
    response = student_client.get(STUDENTS)
    assert response.status_code == 200
    expected = merged(
        dataset["baselines"]["students_by_branch"],
        {"Computer Science": 3, "Mechanical Engineering": 1},
    )
    assert as_count_map(response.get_json()["data"]) == expected


def test_students_analytics_total(student_client, dataset):
    response = student_client.get(STUDENTS, query_string={"all": "true"})
    assert response.status_code == 200
    assert response.get_json()["data"] == [["Total", dataset["baselines"]["students_total"] + 4]]


def test_students_analytics_by_academic_degree(student_client, dataset):
    response = student_client.get(STUDENTS, query_string={"academic_degree": "true"})
    assert response.status_code == 200
    expected = merged(dataset["baselines"]["students_by_degree"], {"B.Tech": 3, "M.Tech": 1})
    assert as_count_map(response.get_json()["data"]) == expected


def test_company_analytics_grouped_by_industry(admin_client, dataset):
    response = admin_client.get(COMPANY)
    assert response.status_code == 200
    expected = merged(
        dataset["baselines"]["company_by_industry"],
        {"Information Technology": 2, "Finance": 1},
    )
    assert as_count_map(response.get_json()["data"]) == expected


def test_company_analytics_total(admin_client, dataset):
    response = admin_client.get(COMPANY, query_string={"all": "true"})
    assert response.status_code == 200
    assert response.get_json()["data"] == [["Total", dataset["baselines"]["company_total"] + 3]]


def test_drives_analytics_default_by_job_type(approved_company_client, dataset):
    response = approved_company_client.get(DRIVES)
    assert response.status_code == 200
    assert sorted_counts(response.get_json()["data"]) == sorted(
        dataset["baselines"]["drives_by_job_type"] + [1, 1, 2]
    )


def test_drives_analytics_by_status(approved_company_client, dataset):
    response = approved_company_client.get(DRIVES, query_string={"by_status": "true"})
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert sum(row[1] for row in data) == dataset["baselines"]["drives_total"] + 4
    assert sorted(count for _, count in data)[-3:] == [1, 1, 2]


def test_drives_analytics_by_company_top_ordering(approved_company_client, dataset):
    response = approved_company_client.get(DRIVES, query_string={"by_company": "true"})
    assert response.status_code == 200
    data = response.get_json()["data"]
    top_label, top_count = data[0]
    assert top_count >= 2
    assert top_label == dataset["companies"][0].company_details.registered_name


def test_drives_analytics_total(approved_company_client, dataset):
    response = approved_company_client.get(DRIVES, query_string={"all": "true"})
    assert response.status_code == 200
    assert response.get_json()["data"] == [["Total", dataset["baselines"]["drives_total"] + 4]]


def test_application_analytics_by_status(student_client, dataset):
    response = student_client.get(APPLICATION)
    assert response.status_code == 200
    data = response.get_json()["data"]
    raw = {str(label): count for label, count in data}
    applied_key = next(key for key in raw if key.endswith("APPLIED"))
    shortlisted_key = next(key for key in raw if key.endswith("SHORTLISTED"))
    assert raw[applied_key] >= 2
    assert raw[shortlisted_key] >= 1


def test_application_analytics_total_with_student_filter(student_client, dataset):
    response = student_client.get(APPLICATION, query_string={"all": "true"})
    assert response.status_code == 200
    assert response.get_json()["data"] == [["Total", dataset["baselines"]["application_total"] + 3]]

    filtered = student_client.get(
        APPLICATION,
        query_string={"all": "true", "student_id": dataset["students"][0].student_details.id},
    )
    assert filtered.status_code == 200
    assert filtered.get_json()["data"] == [["Total", 2]]


def test_placement_analytics_total_and_filters(admin_client, dataset):
    response = admin_client.get(PLACEMENTS, query_string={"all": "true"})
    assert response.status_code == 200
    assert response.get_json()["data"] == [["Total", dataset["baselines"]["placements_total"] + 3]]

    by_company = admin_client.get(
        PLACEMENTS,
        query_string={
            "all": "true",
            "company_id": dataset["companies"][0].company_details.id,
        },
    )
    assert by_company.status_code == 200
    assert by_company.get_json()["data"] == [["Total", 2]]

    by_student = admin_client.get(
        PLACEMENTS,
        query_string={
            "all": "true",
            "student_id": dataset["students"][2].student_details.id,
        },
    )
    assert by_student.status_code == 200
    assert by_student.get_json()["data"] == [["Total", 1]]


def test_placement_analytics_grouped_by_company(admin_client, dataset):
    response = admin_client.get(PLACEMENTS)
    assert response.status_code == 200
    counts = as_count_map(response.get_json()["data"])
    expected_c1 = dataset["companies"][0].company_details.registered_name
    expected_c2 = dataset["companies"][1].company_details.registered_name
    expected = merged(
        dataset["baselines"]["placements_by_company"],
        {expected_c1: 2, expected_c2: 1},
    )
    assert counts == expected


@pytest.mark.parametrize(
    "endpoint",
    [STUDENTS, COMPANY, DRIVES, APPLICATION, PLACEMENTS],
)
def test_analytics_requires_authentication(unauthenticated_client, endpoint):
    response = unauthenticated_client.get(endpoint)
    assert response.status_code == 401
