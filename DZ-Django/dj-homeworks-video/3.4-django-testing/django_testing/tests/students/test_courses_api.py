import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
import json


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get('/api/v1/courses/1/')
    que = response.json()
    assert response.json()['id'] == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get('/api/v1/courses/')
    assert len(response.json()) == 5
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_filtered_course_name(client, course_factory):
    courses = course_factory(_quantity=5)
    name = courses[0].name
    # response = client.get('/api/v1/courses/?name=' + name)
    response = client.get('/api/v1/courses/', {'name': name})
    assert response.json()[0]['name'] == name
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_filtered_course_id(client, course_factory):
    courses = course_factory(_quantity=5)
    id = courses[1].id
    # response = client.get('/api/v1/courses/?id=' + str(id))
    response = client.get('/api/v1/courses/', {'id': id})
    assert response.json()[0]['id'] == id
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'python'})
    assert response.json()['name'] == 'python'
    assert response.status_code == 201

# доделать ниже
@pytest.mark.django_db
def test_patch_course(client, course_factory):
    courses = course_factory(_quantity=5)
    id = courses[0].id
    response = client.patch('/api/v1/courses/' + str(id) + '/', data={'name': 'jaba'})
    assert response.json()['name'] == 'jaba'
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=5)
    id = courses[0].id
    response = client.delete('/api/v1/courses/' + str(id) + '/')
    assert response.status_code == 204