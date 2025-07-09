# viaje_con_mapa.py
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

transportes = {
    "auto": 80,
    "bus": 60,
    "avion": 800
}

geolocator = Nominatim(user_agent="viaje_app")

def obtener_coordenadas(ciudad):
    try:
        ubicacion = geolocator.geocode(ciudad)
        if ubicacion:
            return (ubicacion.latitude, ubicacion.longitude, ubicacion.address)
    except:
        return None

while True:
    print("\n--- Calculadora de Viajes con Mapa ---")
    origen = input("Ciudad de origen o 's' para salir: ").strip().lower()
    if origen == "s":
        break

    destino = input("Ciudad de destino: ").strip().lower()

    origen_data = obtener_coordenadas(origen)
    destino_data = obtener_coordenadas(destino)

    if not origen_data or not destino_data:
        print("No se encontraron una o ambas ciudades.")
        continue

    coord_origen = (origen_data[0], origen_data[1])
    coord_destino = (destino_data[0], destino_data[1])

    distancia_km = geodesic(coord_origen, coord_destino).kilometers
    distancia_millas = geodesic(coord_origen, coord_destino).miles

    print("Medios de transporte disponibles:", ", ".join(transportes.keys()))
    medio = input("Seleccione el medio de transporte: ").strip().lower()

    if medio not in transportes:
        print("Medio de transporte no válido.")
        continue

    duracion = distancia_km / transportes[medio]

    print("\nNarrativa del viaje:")
    print(f"Desde {origen.title()} hasta {destino.title()}")
    print(f"Distancia: {distancia_km:.2f} kilómetros / {distancia_millas:.2f} millas")
    print(f"Duración estimada en {medio}: {duracion:.2f} horas")

    # Crear el mapa centrado entre ambos puntos
    centro_lat = (coord_origen[0] + coord_destino[0]) / 2
    centro_lon = (coord_origen[1] + coord_destino[1]) / 2
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=5)

    # Marcadores
    folium.Marker(coord_origen, popup=f"Origen: {origen_data[2]}", icon=folium.Icon(color='green')).add_to(mapa)
    folium.Marker(coord_destino, popup=f"Destino: {destino_data[2]}", icon=folium.Icon(color='red')).add_to(mapa)

    # Línea entre puntos
    folium.PolyLine([coord_origen, coord_destino], color="blue", weight=2.5, opacity=1).add_to(mapa)

    # Guardar mapa como HTML
    mapa.save("viaje.html")
    print("Mapa guardado en archivo 'viaje.html'. Puedes abrirlo en tu navegador.")





mapa.save(ruta_archivo)
print(f"Mapa guardado en archivo '{ruta_archivo}' en la carpeta:\n{os.getcwd()}")
