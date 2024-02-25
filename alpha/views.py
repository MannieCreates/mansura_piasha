from django.shortcuts import render, redirect
from .models import Item, login_info
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, LoginForm, ForgotPasswordForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

def index(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if the username already exists
            if login_info.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'signup.html', {'form': form})

            # Create user and log in
            # Use create from the user model manager for proper password hashing
            user = login_info.objects.create(
                username=form.cleaned_data['username'],
                age=form.cleaned_data['age'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                security_question=form.cleaned_data['security_question'],
                security_answer=form.cleaned_data['security_answer']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            messages.success(request, 'Account created successfully!')

            return redirect('index')  # Redirect to your homepage
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             # Check if the username already exists
#             if login_info.objects.filter(username=form.cleaned_data['username']).exists():
#                 messages.error(request, 'Username already exists. Please choose a different username.')
#                 return render(request, 'signup.html', {'form': form})

#             # Create user and log in
#             # (Remember to handle password hashing in a real-world scenario)
#             user = login_info.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#                 age = form.cleaned_data['age'],
#                 name=form.cleaned_data['name'],
#                 email=form.cleaned_data['email'],
#                 phone_number=form.cleaned_data['phone_number'],
#                 security_question=form.cleaned_data['security_question'],
#                 security_answer=form.cleaned_data['security_answer']
#             )
#             login(request, user)

#             messages.success(request, 'Account created successfully!')

#             return redirect('index')  # Redirect to your homepage
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to your homepage
            else:
                # Handle invalid login
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            security_question = form.cleaned_data['security_question']
            security_answer = form.cleaned_data['security_answer']

            try:
                user = login_info.objects.get(username=username, security_question=security_question, security_answer=security_answer)
            except login_info.DoesNotExist:
                # Handle incorrect security question or answer
                return render(request, 'forgot_password.html', {'form': form, 'error_message': 'Invalid security question or answer'})

            # Render a new form for setting a new password
            return render(request, 'set_new_password.html', {'user_id': user.id})

    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})

def set_new_password(request, user_id):
    user = login_info.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        # Set the new password (remember to handle password hashing in a real-world scenario)
        user.password = make_password(new_password)
        user.save()

        # Redirect to the login page or any other page
        return redirect('login')

    return render(request, 'set_new_password.html', {'user_id': user_id})