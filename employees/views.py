import json

from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse
from .CallGenerator import BitrixCallGenerator
from views import get_name


@main_auth(on_cookies=True)
def list(request):
    bx = request.bitrix_user_token

    employees = bx.call_list_method('user.get')

    return render(request, 'employees_list.html', {
        'employees': employees
    })


@main_auth(on_cookies=True)
def generate_test_calls(request):
    if request.method == 'POST':
        try:
            bx = request.bitrix_user_token
            generator = BitrixCallGenerator(bx)
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            count = data.get('count')

            if not count:
                JsonResponse({'error': 'Параметр "count" не найден в теле запроса'}, status=400)
            count = int(count)

            result = generator.generate_test_calls(count=count)

            result_to_return = {'status': 'success', 'count_generated': result}

            return JsonResponse(result_to_return)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=400)
