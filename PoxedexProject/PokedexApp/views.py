from urllib.error import HTTPError
from django.shortcuts import render
import urllib.request
import json

# Create your views here.
def index(request):
    try:
        if request.method == 'POST':
            pokemon = request.POST['pokemon'].lower() #Obligar Minisculas en Consulta
            pokemon = pokemon.replace(' ', '%20') #Control de Errores por Espacios en Consulta
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}') # La variable Pokemon
            url_pokeapi.add_header('User-Agent', 'whatever')

            source = urllib.request.urlopen(url_pokeapi).read() #Leer la URL en Formato JSON

            list_of_data = json.loads(source) #Convirtiendo el JSON a un diccionario para ser legible por Python

              # Altura de decímetros a metros
            height_obtained = (float(list_of_data['height']) * 0.1)
            height_rounded = round(height_obtained, 2)

            # Peso de hectogramos a kilogramos
            weight_obtained = (float(list_of_data['weight']) * 0.1)
            weight_rounded = round(weight_obtained, 2)

            data = { #Variable de Renderizacion
                "number": str(list_of_data['id']),
                "name": str(list_of_data['name']).capitalize(),
                "height": str(height_rounded)+ " m",
                "weight": str(weight_rounded)+ " kg",
                "sprite": str(list_of_data['sprites']['front_default']),
            }

            print(data)
        else:
            data = {}
        return render(request, 'main/index.html', data)
    except HTTPError as e:
        if e.code == 404:
            return render(request, 'main/404.html')