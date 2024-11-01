import pandas as pd
from django.shortcuts import render,redirect
from .forms import CropSuggestionForm
import requests
import csv
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the user and log them in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('suggest_crops')  # Redirect to the crop suggestions page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def market_rates_view(request):
    market_data = []
    with open('crops/data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            market_data.append({
                'commodity_name': row['commodity_name'],
                'market_id': row['market_id'],
                'min_price': float(row['min_price']),
                'max_price': float(row['max_price']),
                'modal_price': row['modal_price'],
                'district_name': row['district_name']
            })
    
    # Filtering logic
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    filtered_data = []
    for item in market_data:
        if (query.lower() in item['commodity_name'].lower() or query.lower() in item['district_name'].lower()):
            if (min_price and item['min_price'] < float(min_price)) or (max_price and item['max_price'] > float(max_price)):
                continue
            filtered_data.append(item)

    return render(request, 'market_rates.html', {'market_data': filtered_data, 'query': query, 'min_price': min_price, 'max_price': max_price})

def get_lat_lon(location, api_key):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200 and response.json():
        location_data = response.json()[0]
        return location_data['lat'], location_data['lon']
    return None, None

# Function to get weather data (temperature and humidity) using OpenWeather API
def get_weather_data(lat, lon, api_key):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return temperature, humidity
    return None, None

@login_required# View for crop suggestions
def suggest_crops(request):
    crops = []
    historical_data = pd.read_csv('crops/historical_crop_data.csv')  # Load historical crop data
    if request.method == 'POST':
        form = CropSuggestionForm(request.POST)
        if form.is_valid():
            # Get user input data
            location = form.cleaned_data['location']
            nitrogen = form.cleaned_data['nitrogen']
            phosphorus = form.cleaned_data['phosphorus']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']
            
            # Define your OpenWeather API key
            api_key = '810901f3c70f8754158b4bcc606047db'  # Replace with your actual API key

            # Get latitude and longitude from location
            lat, lon = get_lat_lon(location, api_key)
            if lat is not None and lon is not None:
                # Get temperature and humidity from OpenWeather API
                temperature, humidity = get_weather_data(lat, lon, api_key)
                if temperature is not None and humidity is not None:
                    # Load crop data
                    crop_data = pd.read_csv('crops/crop_data.csv')
                    
                    # Filter crops based on criteria
                    suitable_crops = crop_data[
                        (crop_data['N'] <= nitrogen) &
                        (crop_data['P'] <= phosphorus) &
                        (crop_data['pH'] <= ph) &
                        (crop_data['Rainfall'] <= rainfall) &
                        (crop_data['Temperature'] <= temperature) &
                        (crop_data['Humidity'] <= humidity)
                    ]

                    # Extract unique crop names
                    crops = suitable_crops['Crop'].drop_duplicates().tolist()  # Get unique crop names
                else:
                    form.add_error(None, 'Could not retrieve weather data. Please try again.')
            else:
                form.add_error(None, 'Location not found. Please enter a valid location.')
    else:
        form = CropSuggestionForm()

    return render(request, 'suggested_crops.html', {'form': form, 'crops': crops})

@login_required# View for displaying historical crop data
def historical_data_view(request):
    historical_data = pd.read_csv('crops/historical_crop_data.csv')
    # Assuming you want to display the first 10 rows for brevity
    data_sample = historical_data.sample(n=50, random_state=4)
    return render(request, 'historical_data.html', {'data_sample': data_sample})

@login_required 
def crop_trends_view(request):
    historical_data = pd.read_csv('crops/historical_crop_data.csv')
    # Analyze trends (this is just an example; customize based on your needs)
    crop_trends = historical_data.groupby('Crop')['Production'].sum().reset_index()
    return render(request, 'crop_trends.html', {'crop_trends': crop_trends})
