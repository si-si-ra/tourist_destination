from django.shortcuts import render
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from touristdestinationapp.models import TouristDestination

# Create your views here.
def userview(request):
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

        return render(request, 'userview.html', {'data': data})

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
            return render(request, 'userview.html', context)
        except requests.RequestException as e:
            error_message = f"Error fetching destinations: {str(e)}"
            return render(request, 'userview.html', {'error_message': error_message})
   
        

def view(request, id):
    destination = get_object_or_404(TouristDestination, id=id)
    return render(request, 'view.html', {'destination': destination})

