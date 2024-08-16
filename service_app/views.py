import os
import base64
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .models import Services, CustomUser
from .forms import ServiceForm, RegistrationForm, LoginForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator

def generate_access_token(user):
    return default_token_generator.make_token(user)

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False  # For email verification logic, if needed
            user.save()
            token = generate_access_token(user)
            user.access_token = token
            user.save()
            user_id = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8')

            verification_link = f'http://127.0.0.1:8000/verify/{user_id}/{user.access_token}/'
            admin_email = 'nensi.darji@radixweb.com'
            html_message = render_to_string('email.html', {'forgot_password': verification_link, 'Name': user.username, 'link_title': 'Verification link', 'template_title': "Registered Done!", 'verified_message': 'verify your email address'})
            plain_message = strip_tags(html_message)
            is_send = send_mail(
                'Email Verification',
                plain_message,
                admin_email,
                [user.email],
                html_message=html_message,
                fail_silently=True,
            )
            if is_send == 1:
                # Directly log in the user
                login(request, user)
                return redirect('registration_success')
            else:
                return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/success.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if not email or not password:
                messages.error(request, 'Email and password are required')
                return redirect('login')  # Redirect back to login page with error messages

            user = authenticate(request, email=email, password=password)
            if user is None:
                messages.error(request, 'Incorrect email or password')
                return redirect('login')  # Redirect back to login page with error messages

            if not user.is_verified:
                user_id = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8')
                verification_link = f'http://127.0.0.1:8000/verify/{user_id}/{user.access_token}/'
                messages.error(request, f'Email is not verified <a href="{verification_link}"> Verified link.</a>')
                # You can add an anchor tag to the message here if needed
                return redirect('login')  # Redirect back to login page with error messages

            login(request, user)
            return redirect('get_service')  # Return JSON response for AJAX requests

    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def verify_email(request, userid, token):  # noqa: ARG001
    try:
        user_id = base64.b64decode(userid).decode('utf-8')
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, f'User not found')
        # User not found or already verified
        return redirect('/?status=error', {'status': 'error', 'message': 'User not found'})

    # Compare the generated token with the received token
    if user.is_verified:
        messages.error(request, f'User is already verified')
        return redirect('/?status=error', {'status': 'error', 'message': 'User is already verified'})
    elif token == user.access_token:
        # Token is valid, perform the necessary actions
        user.is_verified = True
        user.save()
        messages.success(request, 'Email verified successfully')
        return redirect('/?status=success', {'status': 'success', 'message': 'Email verified successfully'})
    else:
        messages.error(request, 'Invalid access token')
        return redirect('/?status=error', {'status': 'error', 'message': 'Invalid access token'})

# service crud

def get_service(request):
    get_service_data = Services.objects.all()
    return render(request, 'list.html', {'services': get_service_data})


def add_service(request):
    print(request.method)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Service has been created.")
            return redirect('get_service')
    else:
        form = ServiceForm()
    return redirect('get_service')

def edit_service_modal(request, service_id):
    service = get_object_or_404(Services, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('get_service')  # Redirect to service list page
    else:
        form = ServiceForm(instance=service)
        print(form)
    return render(request, 'edit_service_modal.html', {'service': service})

def delete_service(request, id):
    service = get_object_or_404(Services, pk=id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        # Redirect to appropriate view after deletion
        return redirect('get_service')
