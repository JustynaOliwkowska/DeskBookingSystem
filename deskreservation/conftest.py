import pytest
from django.contrib.auth.models import User
from django.test import Client
from deskreservation.models import OfficeArea, Reservation, OfficeAreaNotice, ReservationNotice

@pytest.fixture
def client():
    client = Client()
    return client

@pytest.fixture
def officearea():
    officea = OfficeArea.objects.create(name='Purple', capacity=30)
    return officea

@pytest.fixture
def officeareas():
    OfficeArea.objects.create(name="Name1", capacity=50)
    OfficeArea.objects.create(name="Name2", capacity=20)
    OfficeArea.objects.create(name="Name3", capacity=30)
    return OfficeArea.objects.all()

@pytest.fixture
def user():
    user = User.objects.create_user(username='sameusername', first_name='NewUser9', last_name='NewUser9',
                                    password='test', email='NewUser19@user.com')
    return user

@pytest.fixture
def area():
    area = OfficeArea.objects.create(name='zonetest', capacity=33)
    return area

@pytest.fixture
def area1():
    area1 = OfficeArea.objects.create(name='Name11', capacity=50)
    return area1

@pytest.fixture
def reservation(area):
    reservation = Reservation.objects.create(date='2020-10-24', area_id=area, employee_id='plu111')
    return reservation

@pytest.fixture
def reservation1(area):
    reservation1 = Reservation.objects.create(date='2020-12-24', area_id=area, employee_id='plu111')
    return reservation1

@pytest.fixture
def officenotice(area):
    officenotice = OfficeAreaNotice.objects.create(to_area=area, content='text')
    return  officenotice

@pytest.fixture
def reservationnotice(reservation):
    reservationnotice = ReservationNotice.objects.create(to_reservation=reservation, content='text123')
    return  reservationnotice


