# weather/views.py

from django.shortcuts import render
import requests
import datetime

def weather_view(request):
    weather_data = None
    daily = []

    # Danh sách các thành phố để hiển thị trong dropdown menu
    cities = ['London', 'New York', 'Paris', 'Tokyo', 'Ha Noi', 'Phu Tho'
              ]

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            api_key = '3e61eb00df9a7492372d4bf66a33f2dd'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'lat' : data['coord']['lat'],
                    'lon' : data['coord']['lon'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                 }
                base_url = "https://api.openweathermap.org/data/2.5/onecall"
                params = {
                    'lat': weather_data['lat'],
                    'lon': weather_data['lon'],
                    'exclude': 'current,minutely,hourly,alerts',
                    'appid': api_key,
                    'units': 'metric'
                }
                res = requests.get(base_url, params=params)
                if(res.status_code == 200):
                    data2 = res.json()
                    for da in data2['daily_data'][:5]:
                        daily.append({
                            'day':datetime.datetime.fromtimestamp(da['dt']).strftime("%A"),
                            'min_temp' : round(da['temp']['min'])
                        })
            else:
                error_message = 'Could not retrieve weather data. Please try again later.'
                return render(request, 'weather/index.html', {'error': error_message, 'cities': cities})

    return render(request, 'weather/index.html', {'weather_data': weather_data, 'cities': cities, 'daily': daily})
