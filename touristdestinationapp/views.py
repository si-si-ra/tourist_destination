from django.shortcuts import render, redirect
from .models import TouristDestination
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import AllowAny
from .forms import TouristDestinationForm
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


class TouristDestinationCreateView(generics.ListCreateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializers
    permission_classes = [AllowAny]


class TouristDestinationDetailView(generics.RetrieveAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializers


class TouristDestinationUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializers


class TouristDestinationDeleteView(generics.DestroyAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializers


class TouristDestinationSearchView(generics.ListAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializers

    def get_queryset(self):
        name = self.kwargs.get('place_name')
        if name:
            return TouristDestination.objects.filter(Place_name__icontains=name)
        return super().get_queryset()


def create_touristdestination(request):
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/tourist/create/'
                data = form.cleaned_data
                print(data)
                image = request.FILES.get('image')

                response = requests.post(api_url, data=data, files={'image': image})

                if response.status_code == 200:
                    messages.success(request, 'Record Inserted Successfully')
                else:
                    messages.error(request, f'Error: {response.status_code}')

            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            # Log form errors for debugging
            messages.error(request, 'Form invalid: ' + str(form.errors))
            print(form.errors)  # Log the errors to console

    else:
        form = TouristDestinationForm()
    return render(request, 'create_tourist_destination.html', {'form': form})




def index(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        api_url = f'http://127.0.0.1:8000/tourist/search/{search}/'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            data = None
            messages.error(request, f"Search request error: {str(e)}")

        return render(request, 'index.html', {'data': data})

    else:
        api_url = 'http://127.0.0.1:8000/tourist/create/'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            original_data = response.json()
            paginator = Paginator(original_data, 6)
            page = request.GET.get('page', 1)

            try:
                touristdestinations = paginator.page(page)
            except (EmptyPage, PageNotAnInteger):
                touristdestinations = paginator.page(1)

            context = {
                'original_data': original_data,
                'touristdestinations': touristdestinations,
            }
            return render(request, 'index.html', context)
        except requests.RequestException as e:
            error_message = f"Error fetching destinations: {str(e)}"
            return render(request, 'index.html', {'error_message': error_message})
   
        


def view_tourist_destination(request, id):
    destination = get_object_or_404(TouristDestination, id=id)
    return render(request, 'view_tourist_destination.html', {'destination': destination})



def update_tourist_destination(request, id):
    # Fetch the specific TouristDestination instance or return a 404 if not found
    destination = get_object_or_404(TouristDestination, id=id)

    if request.method == 'POST':
        # Populate the form with POST data and existing instance to update
        form = TouristDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()  # Save the updated destination
            messages.success(request, 'Destination updated successfully')
            return redirect('destination_list')  # Redirect to the list or detail view
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        # For a GET request, show the form with the current data pre-filled
        form = TouristDestinationForm(instance=destination)

    return render(request, 'update_tourist_destination.html', {'form': form, 'destination': destination})



def delete_tourist_destination(request, id):
    destination = get_object_or_404(TouristDestination, id=id)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted successfully')
        return redirect('destination_list')  # Redirect to list view

    return render(request, 'delete_tourist_destination.html', {'destination': destination})


