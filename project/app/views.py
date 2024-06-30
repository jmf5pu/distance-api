from rest_framework.decorators import api_view
from rest_framework.response import Response
from project.settings import GOOGLE_API_KEY
from app.helpers import calculate_distance, get_coords_tuple, get_geocode_api_results
from app.decorators import api_exception_handler
from app.models import Place
from typing import Optional

@api_view(['POST'])
@api_exception_handler
def get_geocode(request):
    
    raw_address = request.data.get("address")

    place: Optional[Place] = Place.objects.filter(raw_address=raw_address).first()
    if place == None:
        results = get_geocode_api_results(
            {
                'address': raw_address,
                'key': GOOGLE_API_KEY
            }
        )
        place = Place.objects.create(
            raw_address=raw_address,
            formatted_address=results['formatted_address'],
            latitude=results['geometry']['location']['lat'],
            longitude=results['geometry']['location']['lng']
        )

    return Response(
        {
            'latitude': place.latitude,
            'longitude': place.longitude
        }
    )

@api_view(['POST'])
@api_exception_handler
def reverse_geocode(request):
    coords_str = request.data.get("latlng")
    coords = get_coords_tuple(coords_str)

    place: Optional[Place] = Place.objects.filter(
        latitude=coords[0], 
        longitude=coords[1]
    ).first()
    if place == None:
        print("pinging api\n\n\n")
        results = get_geocode_api_results(
            {
                'latlng': coords_str,
                'key': GOOGLE_API_KEY
            }
        )
        place = Place.objects.create(
            raw_address=results['formatted_address'],
            formatted_address=results['formatted_address'],
            latitude=results['geometry']['location']['lat'],
            longitude=results['geometry']['location']['lng']
        )

    return Response(
        {
            'formatted_address': place.formatted_address
        }
    )

@api_view(['GET'])
@api_exception_handler
def calculate_geometric_distance(request):
    start_coords = get_coords_tuple(request.data.get("start"))
    end_coords = get_coords_tuple(request.data.get("end"))
    
    return Response(
        {
            'geometric_distance': calculate_distance(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
        }
    )
