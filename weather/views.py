from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import dotenv_values
import requests
from xml.etree.ElementTree import Element, SubElement, tostring

from .serializers import WeatherSerializer, WeatherResponseSerializer


class WeatherAPIView(APIView):
    def post(self, request):
        serializer = WeatherSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            output_format = serializer.validated_data['output_format']
            env_vars = dotenv_values(".env")
            api_key = env_vars.get("API_KEY")
            url = "https://weatherapi-com.p.rapidapi.com/current.json"
            query = {"q": city}
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=query)

            if response.status_code == 200:
                weather_data = response.json()

                if output_format == 'json':
                    response_data = {
                        "Weather": weather_data['current']['temp_c'],
                        "Latitude": weather_data['location']['lat'],
                        "Longitude": weather_data['location']['lon'],
                        "City": f"{weather_data['location']['name']}, {weather_data['location']['country']}"
                    }
                    serializer = WeatherResponseSerializer(data=response_data)
                    if serializer.is_valid():
                        return Response(serializer.validated_data, status=200)
                    else:
                        return Response(serializer.errors, status=500)
                elif output_format == 'xml':
                    root = Element('root')
                    SubElement(root, 'Temperature').text = str(weather_data['current']['temp_c'])
                    SubElement(root, 'City').text = weather_data['location']['name']
                    SubElement(root, 'Latitude').text = str(weather_data['location']['lat'])
                    SubElement(root, 'Longitude').text = str(weather_data['location']['lon'])
                    xml_response = '<?xml version="1.0" encoding="UTF-8" ?>\n' + tostring(root).decode()
                    return Response(xml_response, status=200, content_type='application/xml')
                else:
                    response_data = {"error": "Invalid output_format. Supported formats: json, xml."}
                    return Response(response_data, status=400)
            else:
                response_data = {"error": "Failed to fetch weather data."}
                return Response(response_data, status=500)
        else:
            return Response(serializer.errors, status=400)
