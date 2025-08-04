from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse
from views import get_name


@main_auth(on_cookies=True)
def list(request):
    bx = request.bitrix_user_token

    employees = bx.call_list_method('user.get')

    return render(request, 'employees_list.html', {
            'employees': employees
        })
