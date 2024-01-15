from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout as auth_logout

from .models import Gun, Order, Payment
from .forms import CreateGunForm, UpdateGunForm

def main(request):
     return render(request, 'main.html')

def login(request):
    page = 'login'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) 
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    else:
        form = AuthenticationForm()

    context = {'page': page, 'form': form}
    return render(request, 'auth/login.html', context)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request) 
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'auth/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('main'))

def home(request):
    return render(request, 'home.html')

# STAFF AND NON-STAFF
def is_staff(user):
    return user.is_authenticated and user.is_staff

def is_not_staff(user):
    return user.is_authenticated and not user.is_staff

# - List
@login_required(login_url='login')
def list(request):
    my_records = Gun.objects.all()
    context = {'records': my_records}
    return render(request, 'admin/list.html', context=context)


# - Create a record 
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def create_record(request):
    form = CreateGunForm()
    if request.method == "POST":
        form = CreateGunForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect('home')
    context = {'form': form}
    return render(request, 'admin/create-gun.html', context=context)


# - Update a record 
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def update_record(request, pk):
    record = Gun.objects.get(id=pk)
    form = UpdateGunForm(instance=record)
    if request.method == 'POST':
        form = UpdateGunForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('home')
    context = {'form':form}
    return render(request, 'admin/update-gun.html', context=context)


# - Read / View a singular record
@login_required(login_url='login')
def singular_record(request, pk):
    gun = Gun.objects.get(id=pk)
    context = {'gun': gun}
    return render(request, 'admin/view-record.html', context=context)



# - Delete a record
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def delete_record(request, pk):
    record = Gun.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted!")
    return redirect('home')


# - Order
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def create_order(request):
    if request.method == "POST":
        gun_id = request.POST["gun"]
        quantity = request.POST["quantity"]
        gun = Gun.objects.get(pk=gun_id)
        order = Order.objects.create(
            user=request.user, 
            gun=gun, 
            quantity=quantity
        )
        return redirect("order_detail", pk=order.pk)
    else:
        gun_list = Gun.objects.all()
        return render(request, "admin/make-order.html", {"gun_list": gun_list})


# - detail
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, "admin/order_detail.html", {"order": order})


# - payment
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def make_payment(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        amount = request.POST["amount"]
        is_payment_less = order.is_payment_less()
        if is_payment_less == False:
            payment = Payment.objects.create(order=order, amount=amount)
            return redirect("dashboard", pk=payment.pk)
        else:
            return HttpResponse("Pembayaran kurang dari total harga")
    else:
        return render(request, "home/make-payment.html", {"order": order})


# - laporan
@login_required(login_url='login')
@user_passes_test(is_staff, login_url='login')
def laporan_transaksi(request):
    payment = Payment.objects.all()
    order = Order.objects.all()
    context = {"payment": payment, "order": order}
    return render(request, "home/laporan_transaksi.html", context)


# #USER
# @login_required(login_url='login')
# @user_passes_test(is_not_staff, login_url='login')
# def list(request):
#     guns = Gun.objects.all()
#     context = {'guns': guns}
#     return render(request, 'list.html', context)