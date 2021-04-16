import json

import requests
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_cors import CorsViewMixin
from tablib import Dataset

from models import DebtorCard


routes = web.RouteTableDef()


@routes.view("/api/name/")
class NameViewSet(web.View, CorsViewMixin):  # TODO naming

    def sort_for_debtor(self, data, company):
        total = dict()
        total['main_company'] = company
        total['personal_account'] = data.get('ACC_CODE')
        total['address_debtor'] = ', '.join([data.get('НАСЕЛЁННЫЙ ПУНКТ'), data.get('ПОДПУНКТ'),
                                             data.get('РАЙОН'), data.get('УЛИЦА'),
                                             data.get('АДРЕС: ДОМ: НОМЕР C ЛИТЕРОЙ'),
                                             str(data.get('КВАРТИРА'))])
        total['full_name'] = data.get('ОТВЕТСТВЕННЫЙ СОБСТВЕННИК')
        total['one_charges'] = data.get('one_charges')
        total['payment_by_receipt'] = data.get('payment_by_receipt')
        total['opening_balance'] = data.get('САЛЬДО ВХОДНОЕ')
        total['assessed'] = data.get('НАЧИСЛЕНИЕ ПОЛНОЕ')
        total['paid'] = data.get('ОПЛАТА')
        total['start_time'] = str(data.get('ДАТА ОТКРЫТИЯ'))[:10].replace('-', '.')
        if data.get('ДАТА ЗАКРЫТИЯ', False):
            total['end_time'] = str(data.get('ДАТА ЗАКРЫТИЯ'))[:10].replace('-', '.')
        total['debt_calculation'] = data.get('перерасчет')

        return total

    async def post(self):
        data = await self.request.json()
        check = True
        company = data['company']
        field_array = [
            "personal_account", "other_info", "address_debtor", "jurisdiction", "court_details",
            "full_name","num_of_passport", "inn_debtor", "opening_balance", "assessed", "one_charges",
            "paid", "payment_by_receipt", "debt_calculation", "peni_calc_155", "peni_calc_395", "state_fees_calc",
            "debt_data", "validation"
        ]  # TODO check fields
        try:
            accessed_formats = ['csv', 'xls', 'xlsx']
            dataset = Dataset()
            new_words = data['importData']
            file_format = new_words.name.split('.')[-1]

            # проверка на соответствие форматам
            if file_format in accessed_formats:

                # чтение файлов
                if file_format == 'csv':
                    imported_data = dataset.load(new_words.read().decode('utf-8'), format=file_format)
                else:
                    imported_data = dataset.load(new_words.read(), format=file_format)

                # проверка на соответствие шаблона
                for debtor in json.loads(imported_data.get_json()):
                    for key in debtor.keys():
                        if key not in [field.name for field in field_array]:
                            check = False

                for debtor in json.loads(imported_data.get_json()):

                    # подготовка JSON'ов котправке
                    if debtor.get('id', False):
                        debtor.pop('id')

                    # проверка на соответствие шаблону
                    if not check:
                        debtor = self.sort_for_debtor(debtor, company)

                    # проверка на уникальность  TODO check validate
                    if len(DebtorCard.query.where(DebtorCard.personal_account == debtor['personal_account']).gino.all()) == 0:
                        debtor['main_company'] = company

                        # отправка запроса
                        requests.post(f'http://127.0.0.1:8000/api/debtor_cards/', data=debtor)

                return json_response({'success': True}, status=200)
            else:
                return json_response({'error': 'only {} accepted'.format(', '.join(accessed_formats))}, status=200)
        except Exception as e:
            return json_response({'success': False, 'except': str(e)}, status=500)
