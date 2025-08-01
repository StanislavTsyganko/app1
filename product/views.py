from django.shortcuts import render, get_object_or_404

from integration_utils.bitrix24.bitrix_token import BitrixToken
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse, HttpResponse
from django.core.signing import Signer
from .models import ProductLink
import qrcode
from io import BytesIO
import base64
import requests
from django.core.signing import BadSignature

@main_auth(on_cookies=True)
def generate_url(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        product = ProductLink.create_for_product(product_id=product_id)

        qr_url = f"http://127.0.0.1:8000/product/product_page/{product}"
        img = qrcode.make(qr_url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_image = base64.b64encode(buffer.getvalue()).decode()

        return render(request, 'generate_url.html', {'qr_url': qr_url, 'qr_image': qr_image})

    return render(request, 'generate_url.html')


def product_page(request, uuid):
    try:
        link = get_object_or_404(ProductLink, uuid=uuid)
        product_id = link.product_id
        webhook_url = "https://b24-5qaq29.bitrix24.ru/rest/1/ixtsyettc8qdyiig"

        product_response = requests.get(
            f"{webhook_url}/crm.product.get",
            params={"id": product_id}
        )
        product_data = product_response.json()

        if 'error' in product_data:
            print(f"Ошибка получения товара: {product_data['error_description']}")
            product_data = {}
        else:
            product_data = product_data.get('result', {})

        photo_response = requests.get(
            f"{webhook_url}/catalog.productImage.list",
            params={
                "productId": product_id
            }
        )

        photo_data = photo_response.json()

        image_url = None
        if 'error' not in photo_data:
            photos = photo_data.get('result', {}).get('productImages', [])
            if photos:
                image_url = photos[0].get('detailUrl')
                if image_url and not image_url.startswith(('http://', 'https://')):
                    image_url = f"https://b24-5qaq29.bitrix24.ru{image_url}"

        return render(request, 'show_product.html', {
            'product': product_data,
            'image_url': image_url
        })

    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        return render(request, 'error.html', status=500)
