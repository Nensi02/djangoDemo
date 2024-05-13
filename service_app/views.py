from django.shortcuts import render, redirect, get_object_or_404
from .models import Services
from .forms import ServiceForm
from django.contrib import messages

# Create your views here.
def get_service(request):
    get_service_data = Services.objects.all()
    return render(request, 'list.html', {'services': get_service_data})

def add_service(request):
    print(request.method)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
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
    return render(request, 'edit_service_modal.html', {'form': form, 'service': service})

def delete_service(request, id):
    service = get_object_or_404(Services, pk=id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('get_service')  # Redirect to appropriate view after deletion