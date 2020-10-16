"""desk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from deskreservation.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginUserView.as_view(), name="index0"),
    path('main/', MainPage2.as_view(), name="main"),
    path('logout_user/', LogoutView.as_view(), name="logout-user"),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('list_users/', ListUsersView.as_view(), name="list_users"),
    path('add/area/', add_area),
    path('show/areas/', show_areas),
    path('desk/reservation/<int:id>', desk_reservation),
    path('reservation/details/<int:id>', desk_details),
    path('reservation/details2/', reservation_details2),
    path('remove/area/<int:id>', delete_area),
    path('remove/desk/<int:id>', delete_desk),
    path('user_search/', UserSearchView.as_view(), name="student-search"),
    path('date_search/', DateAreaSearchView.as_view(), name="date-search"),
    path('area_notice/', AreaMessageView.as_view(), name="notice1"),
    path('reservation_notice/', ReservationMessageView.as_view(), name="notice2"),
    path('area_view/', OfficeAreaNoticeView.as_view(), name='test1'),
    path('reservation_view/', ReservationNoticeView.as_view(), name='test2'),
    path('office/', Office.as_view(), name="main2"),
    path('delete_notice/<int:notice_id>/', DeleteOfficeNote.as_view(), name="main3"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
