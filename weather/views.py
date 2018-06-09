import requests
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import City
from .forms import CityForm
from datetime import datetime
from django.http import HttpResponse

# Create your views here.
def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=311938d6fd8e41c0989b947629b15b44'

	current = datetime.now()
	myday = current.strftime("%a,%d %B,%y")
	#mytime = current.strftime("%X")
	mytime = current.strftime("%I:%M:%S %p")
	total = myday+' , '+mytime



	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()
		return redirect('weatherapp:index')

	form = CityForm()

	cities = City.objects.all()
	weather_data = []
	for city in cities:
		r = requests.get(url.format(city)).json()
		ftemp = r['main']['temp']
		ctemp = Decimal((ftemp-32)*5/9)
		ctemp = round(ctemp,2)
		city_weather = {
		   'city': city.name,
		   'temperature': ctemp,
		   'description': r['weather'][0]['description'],
		   'icon': r['weather'][0]['icon']
		}
		weather_data.append(city_weather)
	#print(weather_data)
	context = {'weather_data': weather_data, 'form': form, 'total': total}
	return render(request, 'weather/basic.html', context)



def details(request, name):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=311938d6fd8e41c0989b947629b15b44'
	cityname = City.objects.get(name=name)
	r = requests.get(url.format(cityname)).json()
	# Temperature from Fahrenheit to Celsius
	ftemp = r['main']['temp']
	ctemp = Decimal((ftemp-32)*5/9)
	ctemp = round(ctemp,2)
	# Minimum Temperature from Fahrenheit to Celsius
	fmintemp = r['main']['temp_min']
	cmintemp = Decimal((fmintemp-32)*5/9)
	cmintemp = round(cmintemp,2)
	# Maximum Temperature from Fahrenheit to Celsius
	fmaxtemp = r['main']['temp_max']
	cmaxtemp = Decimal((fmaxtemp-32)*5/9)
	cmaxtemp = round(cmaxtemp,2)
	# Co-ordinates - Longitude & Latitude
	city_longitude = r['coord']['lon']
	city_latitude = r['coord']['lat']
	# City Weather Description
	description = r['weather'][0]['description']
	# City Weather - pressure, humidity, visibility, wind
	pressure = r['main']['pressure']
	humidity = r['main']['humidity']
	visibility = r['visibility']
	wind_speed = r['wind']['speed']
	wind_degree = r['wind']['deg']
	# City - Country, Sunrise, Sunset
	country = r['sys']['country']
	sunrise = r['sys']['sunrise']
	sunset = r['sys']['sunset']
	# Creating Dictionary
	city_details = {
	  'city': cityname,
	  'temperature': ctemp,
	  'mintemp': cmintemp,
	  'maxtemp': cmaxtemp,
	  'longitude': city_longitude,
	  'latitude': city_latitude,
	  'description': description,
	  'pressure': pressure,
	  'humidity': humidity,
	  'visibility': visibility,
	  'windspeed': wind_speed,
	  'winddegree': wind_degree,
	  'country': country,
	  'sunrise': sunrise,
	  'sunset': sunset
	}
	return render(request, 'weather/citydetails.html', {'city_details': city_details})
