import pytest
from django.contrib.auth.models import User
from django.test import Client
from deskreservation.models import OfficeArea, Reservation

@pytest.mark.django_db
def test_main_page(client):
    url = ''
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_officearea_in_db(client, officearea):
    assert OfficeArea.objects.count() == 1


@pytest.mark.django_db
def test_total_officearea_in_db(client, officeareas):
    assert OfficeArea.objects.count() == 3


@pytest.mark.django_db
def test_officearea_add(client):
    url = '/add/area/'
    assert OfficeArea.objects.count() == 0
    response = client.post(url, {'name': 'White', 'capacity': 60})
    assert response.status_code == 200
    assert OfficeArea.objects.count() == 1
    p = OfficeArea.objects.get(name='White')
    assert p.capacity == 60


@pytest.mark.django_db
def test_add_user(client):
    url = '/add_user/'
    assert User.objects.count() == 0
    response = client.post(url, {'username': 'NewUser1', 'password1': 'NewUser1', 'password2': 'NewUser1',
                                 'first_name': 'NewUser1', 'last_name': 'NewUser1', 'e_mail': 'NewUser1@user.com'})
    assert User.objects.count() == 1
    assert response.status_code == 302
    j = User.objects.get(username='NewUser1')
    assert j.email == 'NewUser1@user.com'


@pytest.mark.django_db
def test_check_if_same_password_provided(client):
    url = '/add_user/'
    response = client.post(url, {'username': 'new_user', 'first_name': 'Justyna', 'last_name': 'Oliwkowska',
                                 'password1': 'test1', 'password2': 'test2', 'e_mail': 'justyna@oliwkowska.pl'})
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_check_if_user_exists(client, user):
    url = '/add_user/'
    assert User.objects.count() == 1
    response = client.post(url, {'username': 'sameusername', 'first_name': 'NewUser9', 'last_name': 'NewUser9',
                                 'password1': 'NewUser9', 'password2': 'NewUser9', 'e_mail': 'NewUser19@user.com'})
    assert response.status_code == 200
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_past_date_reservation(client, reservation, area):
    url = f'/desk/reservation/{area.id}'
    assert Reservation.objects.count() == 1
    response = client.post(url, {'date': '2020-10-10', 'area_id': 'area', 'employee_id': 'plu111'})
    assert response.status_code == 200
    assert Reservation.objects.count() == 1


@pytest.mark.django_db
def test_duplicate_reservation(client, reservation, area):
    url = f'/desk/reservation/{area.id}'
    assert Reservation.objects.count() == 1
    response = client.post(url, {'date': 2020-10-24, 'area_id': area.id, 'employee_id': 'plu111'})
    assert response.status_code == 200
    assert Reservation.objects.count() == 1


@pytest.mark.django_db
def test_capacity(client, area):
    url = '/show/areas/'
    response = client.get(url)
    assert response.status_code == 200
    k = area
    assert k.capacity == 33


@pytest.mark.django_db
def test_reservation_date(client, reservation):
    k = reservation
    assert k.date == '2020-10-24'


@pytest.mark.django_db
def test_delete_area(client, area1):
    response = client.delete(f"/remove/area/{area1.id}")
    assert response.status_code == 200
    area_ids = OfficeArea.objects.all()
    assert area1.id not in area_ids

@pytest.mark.django_db
def test_delete_desk(client, reservation1):
    response = client.delete(f"/remove/desk/{reservation1.id}")
    assert response.status_code == 200
    reservation_ids = Reservation.objects.all()
    assert reservation1.id not in reservation_ids


@pytest.mark.django_db
def test_login_app(client):
    client.login(username='justa33', password='1234')
    response = client.get("/", follow=True)
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_app(client):
    url = '/logout_user/'
    response = client.get(url)
    assert response.status_code == 200

