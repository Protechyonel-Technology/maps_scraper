import requests
import openpyxl
import time


def fetch_places(api_key, query, location="41.0082,28.9784", radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={query}&key={api_key}"
    places = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            places.extend(result.get('results', []))
            next_page_token = result.get('next_page_token')
            if next_page_token:
                time.sleep(2)
                url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"
            else:
                url = None
        else:
            return None
    return places


def fetch_place_details(api_key, place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result', {})
    else:
        return None


def write_to_excel(data, filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["İsim", "Adres", "Telefon Numarası", "Kategori", "Email", "Website"])

    for place in data:
        name = place.get('name')
        address = place.get('vicinity')
        phone_number = place.get('formatted_phone_number', 'N/A')
        category = ', '.join(place.get('types', []))
        email = place.get('email', 'N/A')  # Email bilgisi genellikle API'de mevcut değil
        website = place.get('website', 'N/A')

        sheet.append([name, address, phone_number, category, email, website])

    workbook.save(filename)


api_key = input("API anahtarınızı girin: ")
query = input("Aramak istediğiniz kategoriyi girin: ")

places = fetch_places(api_key, query, location="41.0082,28.9784")
detailed_places = []

if places:
    for place in places:
        place_id = place.get('place_id')
        details = fetch_place_details(api_key, place_id)
        if details:
            detailed_places.append(details)

    filename = f"{query.replace(' ', '_')}.xlsx"
    write_to_excel(detailed_places, filename)
    print(f"Veriler {filename} dosyasına yazıldı.")
else:
    print("Veri çekme işlemi başarısız oldu.")
