from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import JsonResponse
from views import get_name

@main_auth(on_cookies=True)
def list(request):
    try:
        bx = request.bitrix_user_token
        deals = bx.call_list_method('crm.deal.list', {
            'filter': {'ASSIGNED_BY_ID': bx.user_id, 'STAGE_ID': 'PREPARATION'},
            'select': ['ID', 'TITLE', 'STAGE_ID', 'OPPORTUNITY', 'DATE_CREATE'],
            'order': {'DATE_CREATE': 'DESC'},
            'start': 0
        })[:10]

        full_name = get_name(request)

        return render(request, 'list.html', {
            'user': full_name,
            'deals': deals,
            'user_id': bx.user_id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def add(request):
    return
