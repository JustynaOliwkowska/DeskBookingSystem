from datetime import datetime
import datetime
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .forms import LoginUserForm, AddUserForm
from deskreservation.models import OfficeArea, Reservation


# class MainPage(View):
#     def get(self, request):
#         return render(request, 'base.html')

class MainPage2(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginUserView(FormView):
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
    def get(self, request):
        logout(request)
        return HttpResponse("You have been logged out")

class AddUserView(FormView):
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
    template_name = 'list_view.html'
    model = User

def add_area(request):
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


def show_areas(request):
    areas = OfficeArea.objects.all()
    return render(request, "show_areas.html", {'areas': areas})


def desk_reservation(request, id):
    if request.method == 'GET':
        return render(request, 'desk_reservation.html')
    else:
        area = OfficeArea.objects.get(id=id)
        date = request.POST.get("date")
        comment = request.POST.get("comment")
        if str(date) < str(datetime.date.today()):
            return HttpResponse("Past date!")

        res = Reservation.objects.create(date=date, area_id=area,  employee_id=comment)
        res.save()
        message = 'Desk reserved successfully'
        return render(request, 'desk_reservation.html', context={'message': message})

def desk_details(request, id):
    area = OfficeArea.objects.get(id=id)
    reservations = area.reservation_set.filter(date__gte=datetime.date.today()).order_by('date')
    return render(request, 'reservation_details2.html', context={"area": area, "reservations": reservations})

def reservation_details2(request):
    areas = OfficeArea.objects.all()
    return render(request, "reservation_details.html", {'areas': areas})