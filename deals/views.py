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
            'select': ['ID', 'TITLE', 'STAGE_ID', 'OPPORTUNITY', 'DATE_CREATE', 'UF_CRM_1753952380740'],
            'order': {'DATE_CREATE': 'DESC'},
            'start': 0
        })[:10]

        full_name = get_name(request)

        return render(request, 'deals_list.html', {
            'user': full_name,
            'deals': deals,
            'user_id': bx.user_id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@main_auth(on_cookies=True)
def add(request):
    if request.method == 'POST':
        try:
            bx = request.bitrix_user_token
            deal_data = {
                'TITLE': request.POST.get('title'),
                'TYPE_ID': request.POST.get('type_id', 'SALE'),
                'STAGE_ID': request.POST.get('stage_id', 'PREPARATION'),
                'OPPORTUNITY': request.POST.get('amount'),
                'ASSIGNED_BY_ID': bx.user_id,
                'COMMENTS': request.POST.get('comments'),
                'UF_CRM_1753952380740': request.POST.get('url_object')
            }

            result = bx.call_api_method('crm.deal.add', {'fields': deal_data})
            deal_id = result['result'] if isinstance(result, dict) else result

            return JsonResponse({
                'status': 'success',
                'deal_id': deal_id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    full_name = get_name(request)

    return render(request, 'add_deal.html', {'user': full_name})
