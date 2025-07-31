from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import redirect


# @xframe_options_exempt
@main_auth(on_cookies=True)
def main_page(request):
    try:
        if not hasattr(request, 'bitrix_user_token'):
            return

        full_name = get_name(request)

        return render(request, 'main_page.html', {
            'user': full_name
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_name(request):
    user = request.bitrix_user_token
    user_data = user.call_api_method('user.get', {
        'ID': user.user_id
    })
    result = user_data.get('result', [{}])[0]
    first_name = result.get('NAME', '')
    last_name = result.get('LAST_NAME', '')

    full_name = f"{last_name} {first_name}".strip()

    return full_name if full_name else 'Пользователь'
