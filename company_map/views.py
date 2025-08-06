import json
import requests
from django.shortcuts import render
from django.core.cache import cache
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse


@main_auth(on_cookies=True)
def show(request):
    bx = request.bitrix_user_token

    companies = bx.call_list_method('crm.company.list', {
        "SELECT": ['ID', 'ADDRESS', 'TITLE', 'LOGO', 'COMPANY_TYPE']
    })

    for company in companies:
        address = bx.call_list_method('crm.address.list', {
            "FILTER": {"ENTITY_ID": company['ID'], "TYPE_ID": 1}
        })
        if address and address[0]:
            company['ADDRESS'] = format_address(address[0])
        if company['LOGO']:
            company['LOGO'] = f"https://b24-5qaq29.bitrix24.ru{company['LOGO']['downloadUrl']}"

    return render(request, 'show_companies.html', {
        'companies': json.dumps([c for c in companies if c['ADDRESS']])
    })


def clean_string(s):
    if not s:
        return None
    return str(s).translate(
        str.maketrans('', '', '«»№"\'')
    ).strip()


def format_address(address_data):
    city = clean_string(address_data.get('CITY'))
    address_1 = clean_string(address_data.get('ADDRESS_1'))
    address_2 = clean_string(address_data.get('ADDRESS_2'))

    address_parts = []
    if city:
        address_parts.append(city)
    if address_1:
        address_parts.append(address_1)
    if address_2:
        address_parts.append(address_2)

    return ', '.join(address_parts) if address_parts else None


def geocode(request):
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'Address required'},
                            content_type='application/json', status=400)

    api_key = '5ea1a43a-e737-45b0-850e-ef405223dae5'

    try:
        response = requests.get(
            'https://geocode-maps.yandex.ru/1.x/',
            params={
                'apikey': api_key,
                'format': 'json',
                'geocode': address,
                'lang': 'ru_RU'
            },
            timeout=10
        )

        if response.status_code == 403:
            return JsonResponse(
                {'error': 'Access denied by Yandex. Check API key'},
                status=502
            )

        response.raise_for_status()

        data = response.json()

        if not data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember'):
            return JsonResponse({'error': 'Invalid API response structure'},
                                content_type='application/json', status=400)

        feature = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']

        lon, lat = map(float, feature['Point']['pos'].split(' '))

        result = {
            'lat': lat,
            'lon': lon,
            'address': feature['metaDataProperty']['GeocoderMetaData']['text']
        }

        return JsonResponse(result,
                            content_type='application/json')

    except Exception as e:
        return JsonResponse({'error': str(e)},
                            content_type='application/json', status=500)
