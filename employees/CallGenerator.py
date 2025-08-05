import random
import datetime
from django.utils import timezone

from faker import Faker


class BitrixCallGenerator:
    def __init__(self, admin_token):
        self.but = admin_token
        self.fake = Faker('ru_RU')

    def _generate_phone_number(self):
        return f"+7{random.choice(['9', '8'])}{random.randint(100000000, 999999999)}"

    def _get_active_users(self):
        users = self.but.call_list_method('user.get', {
            'FILTER': {'ACTIVE': 'Y'},
            'SELECT': ['ID', 'NAME', 'LAST_NAME', 'WORK_POSITION']
        })
        return users or []

    def _generate_call_data(self, user_id):
        call_start = timezone.now() - datetime.timedelta(
            minutes=random.randint(1, 1440)
        )

        return {
            'USER_ID': user_id,
            'USER_PHONE_INNER': self._generate_phone_number(),
            'PHONE_NUMBER': self._generate_phone_number(),
            'DURATION': random.choices(
                [0, 30, 60, 120, 180, 300],
                weights=[5, 10, 30, 30, 20, 5]
            )[0],
            'CALL_START_DATE': call_start.isoformat(),
            'TYPE': 1,
            'STATUS_CODE': 200
        }

    def generate_test_calls(self, count=10):
        users = self._get_active_users()
        success_count = 0
        if not users:
            print("No active users found")
            return

        for _ in range(count):
            try:
                user = random.choice(users)
                call_data = self._generate_call_data(user['ID'])

                call = self.but.call_list_method(
                    'telephony.externalcall.register',
                    {'USER_ID': call_data['USER_ID'], 'USER_PHONE_INNER': call_data['USER_PHONE_INNER'],
                     'PHONE_NUMBER': call_data['PHONE_NUMBER'], 'TYPE': call_data['TYPE'],
                     'CALL_START_DATE': call_data['CALL_START_DATE']}
                )

                end_call = self.but.call_list_method(
                    'telephony.externalcall.finish',
                    {'USER_ID': call_data['USER_ID'], 'CALL_ID': call['CALL_ID'],
                     'DURATION': call_data['DURATION'], 'STATUS_CODE': call_data['STATUS_CODE']}
                )
                success_count += 1
            except Exception as e:
                print(f"Error generating call for user - {str(e)}")

        return success_count
