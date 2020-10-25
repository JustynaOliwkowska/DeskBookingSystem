from datetime import datetime
import datetime
from django.views.generic import ListView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .forms import LoginUserForm, AddUserForm, UserSearchForm, DateAreaSearchForm, ReservationNoticeForm, \
    OfficeAreaNoticeForm
from deskreservation.models import OfficeArea, Reservation, OfficeAreaNotice
from django.db import IntegrityError


class MainPage(View):
    """
    Main page view after registration
    """
    def get(self, request):
        return render(request, 'index.html')

class LoginUserView(FormView):
    """
    User login view
    """
    template_name = 'login_user.html'
    form_class = LoginUserForm
    success_url = '/main/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("User is not valid")
        return super(LoginUserView, self).form_valid(form)

class LogoutView(View):
    """
    User logout view
    """
    def get(self, request):
        logout(request)
        return HttpResponse("You have been logged out")

class AddUserView(FormView):
    """
    New user adding view
    """
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        new_user = form.cleaned_data['username']
        new_password = form.cleaned_data['password2']
        new_email = form.cleaned_data['e_mail']

        user = User.objects.create_user(username=new_user, password=new_password, email=new_email)
        return super(AddUserView, self).form_valid(form)

class ListUsersView(ListView):
    """
    All users view
    """
    template_name = 'list_view.html'
    model = User

def add_area(request):
    """
    The possibility of adding a new zone in the office
    """
    areas = OfficeArea.objects.all()
    if request.method == 'GET':
        return render(request, 'add_area.html')

    if request.method == 'POST':
        name = request.POST.get('name')
        if name == "":
            message = 'Office Area name cannot be empty'
            return render(request, 'add_area.html', context={'message': message})
        else:
            for area in areas:
                if area.name == name:
                    message = 'Office Area name already exist! Please create different one'
                    return render(request, 'add_area.html', context={'message': message})
        capacity = int(request.POST.get('capacity'))
        if capacity <= 0:
            message = 'Capacity larger than 0'
            return render(request, 'add_area.html', context={'message': message})

    j = OfficeArea.objects.create(name=name, capacity=capacity)
    j.save()
    message = '"Office Area" added successfully'
    return render(request, 'add_area.html', context={'message': message})

class Office(View):
    """
    Office illustration layout
    """
    def get(self, request):
        return render(request, 'office.html')

def show_areas(request):
    """
    All office areas view
    """
    areas = OfficeArea.objects.all()
    return render(request, "show_areas.html", {'areas': areas})

def desk_reservation(request, id):
    """
    Desk reservation in a given zone
    """
    if request.method == 'GET':
        return render(request, 'desk_reservation.html')
    else:
        try:
            area = OfficeArea.objects.get(id=id)
            date = request.POST.get("date")
            comment = request.POST.get("comment")
            if str(date) < str(datetime.date.today()):
                return HttpResponse("Past date!")
            capa = area.capacity
            all_res = Reservation.objects.all().filter(date=date).filter(area_id=area)
            just = capa - len(all_res)
            if just <= 0:
                return HttpResponse("Too many reservation per day!")
            res = Reservation.objects.create(date=date, area_id=area, employee_id=comment)
            res.save()
        except IntegrityError as j:
            return HttpResponse(f'Reservation already done! Error name--> {str(j)}')
        message = 'Desk reserved successfully'
        return render(request, 'desk_reservation.html', context={'message': message})

def desk_details(request, id):
    """
    Detailed desk reservation view
    """
    area = OfficeArea.objects.get(id=id)
    reservations = area.reservation_set.filter(date__gte=datetime.date.today()).order_by('date')
    return render(request, 'reservation_details.html', context={"area": area, "reservations": reservations})

def reservation_details2(request):
    """
    Detailed area reservation view
    """
    areas = OfficeArea.objects.all()
    return render(request, "reservation_details2.html", {'areas': areas})

def delete_area(request, id):
    """
    Office aea delete option
    """
    if request.method == 'GET':
        del_area = OfficeArea.objects.get(id=id)
        del_area.delete()
    message = 'Area removed successfully'
    return render(request, 'remove_area.html', context={'message': message})

def delete_desk(request, id):
    """
    Reserved desk delete option
    """
    if request.method == 'GET':
        del_desk = Reservation.objects.get(id=id)
        del_desk.delete()
    message = 'Desk removed successfully'
    return render(request, 'remove_desk.html', context={'message': message})

class UserSearchView(View):
    """
    Employee ID search option
    """
    def get(self, request):
        form = UserSearchForm()
        return render(request, 'user_search.html', {'form': form})

    def post(self, request):
        form = UserSearchForm(request.POST)
        if form.is_valid():
            users = Reservation.objects.filter(employee_id=form.cleaned_data['employee_id']).filter(
                date__gte=str(datetime.date.today())).order_by('date')

            return render(request, 'user_search.html', {'form': form, 'users': users})
        return render(request, 'user_search.html', {'form': form})

class DateAreaSearchView(View):
    """
    Date search option to indicate all bookings on a given day
    """
    def get(self, request):
        form = DateAreaSearchForm()
        return render(request, 'date_search.html', {'form': form})

    def post(self, request):
        form = DateAreaSearchForm(request.POST)
        if form.is_valid():
            ids = Reservation.objects.filter(date=form.cleaned_data['date'])
            return render(request, 'date_search.html', {'form': form, 'ids': ids})
        return render(request, 'date_search.html', {'form': form})

class AreaMessageView(FormView):
    """
    Additional option to leave comments on a given zone
    """
    template_name = 'message.html'
    form_class = OfficeAreaNoticeForm
    success_url = '/main/'

    def form_valid(self, form):
        form.save()
        return super(AreaMessageView, self).form_valid(form)

class OfficeAreaNoticeView(View):
    """
    All office areas messages view
    """
    def get(self, request):
        to_area = OfficeArea.objects.all()
        return render(request, 'all_notices.html', {'to_area': to_area})

class DeleteOfficeNote(DeleteView):
    """
    Delete office area message view - super user permission required
    """
    template_name = 'delete_officenote.html'
    model = OfficeAreaNotice
    success_url = '/main/'

class ReservationMessageView(FormView):
    """
    Form for an additional option to leave comments on a given reservation
    """
    template_name = 'message.html'
    form_class = ReservationNoticeForm
    success_url = '/main/'

    def form_valid(self, form):
        form.save()
        return super(ReservationMessageView, self).form_valid(form)

class ReservationNoticeView(View):
    """
    All reservation messages view
    """
    def get(self, request):
        to_reservation = Reservation.objects.all()
        return render(request, 'all_notices1.html', {'to_reservation': to_reservation})
