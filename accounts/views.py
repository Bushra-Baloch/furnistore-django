from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ----------------------------
# USER PROFILE
# ----------------------------
@login_required
def profile_view(request):

    profile = request.user.profile
    orders = request.user.orders.all()

    context = {
        "profile": profile,
        "orders": orders
    }

    return render(request, "accounts/profile.html", context)

# ----------------------------
# LOGIN
# ----------------------------
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


# ----------------------------
# REGISTER
# ----------------------------
def register_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, "Account created successfully")

        return redirect('home')

    return render(request, 'accounts/register.html')


# ----------------------------
# LOGOUT
# ----------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


from django.contrib.auth.decorators import login_required


# ----------------------------
# EDIT PROFILE
# ----------------------------
@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        request.user.email = request.POST.get("email")

        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.city = request.POST.get("city")

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully")

        return redirect("profile")

    context = {
        "profile": profile
    }

    return render(request, "accounts/edit_profile.html", context)