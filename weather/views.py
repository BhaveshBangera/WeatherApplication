import requests
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import City
from .forms import CityForm
from datetime import datetime

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



# def example(request):
# 	return render(request, 'weather/basic.html')
