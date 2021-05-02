import asyncio
import datetime
import json

import requests
from gino import Gino

from local_settings import DATABASE
from local_settings import KEY_ROSREESTR


db = Gino()


class DebtorCard(db.Model):
    __tablename__ = 'debtorcard'

    id = db.Column(db.Integer(), primary_key=True)

    personal_account = db.Column()
    other_info = db.Column()
    address_debtor = db.Column()
    jurisdiction = db.Column()
    court_details = db.Column()
    full_name = db.Column()
    num_of_passport = db.Column()
    inn_debtor = db.Column()
    opening_balance = db.Column()
    assessed = db.Column()
    one_charges = db.Column()
    paid = db.Column()
    paid_data = db.Column()
    payment_by_receipt = db.Column()
    debt_calculation = db.Column()
    debt_value = db.Column()
    peni_calc_155 = db.Column()
    peni_calc_395 = db.Column()
    state_fees_calc = db.Column()
    debt_data = db.Column()
    validation = db.Column()
    start_time = db.Column()
    end_time = db.Column()
    
    
class Debtor(db.Model):
    __tablename__ = 'debtor'
    
    id = db.Column(db.Integer(), primary_key=True)
    debtor = db.Column()
    status_order = db.Column()
    query_num = db.Column()


class BaseLogicDebtorMixin:
    async def check_order(self, debtor, key=KEY_ROSREESTR):
        request = requests.post("api/check_order_status/", json={

            "egrn_key": debtor.egrn_key,
            "key": key,
            "parse_egrn_status": True,
            "query_num": debtor.query_num

        })
        result = json.loads(request.content)
        debtor.update(status_order=result["status"]).apply()


    def calculate_155(self, debt: float, days: int, percent: float, share: float):
        """
            пени, взыскиваемые с должника по ст. 155 ЖК РФ

            :param debt: сумма задолженности
            :param days: количество дней просрочки (рассчитывается с даты наступления задолженности и до
            даты погашения включительно)
            :param percent: процентная ключевая ставка Банка России, действующая в период просрочки
            :param share: доля ставки**

            :return: сумма долга
        """

        return debt*days*percent*share

    def day_calculate(self, data_start: str, data_end: str):
        data_start = datetime.datetime.strptime(data_start, '%d.%m.%Y')
        data_end = datetime.datetime.strptime(data_end, '%d.%m.%Y')

        return (data_end - data_start).days


class BaseLogicDebtor(BaseLogicDebtorMixin):
    async def check_reestr(self):
        all_debtor = await Debtor.query.gino.all()
        debtors = [self.check_order(debtor) for debtor in all_debtor]

    async def check_percent(self,  days):
        if days > 90:
            return 1/130
        return 1/300

    async def get_share(self, summa):
        return (summa/100)*5  # TODO change 5 to incorrect value

    async def peny_validate(self, debtor_card):
        _days = self.day_calculate(debtor_card.start_time, debtor_card.end_time)
        if not _days and _days < 0:
            return False

        _percent = await self.check_percent(_days)
        _share = await self.get_share(debtor_card.debt_value)

        _peni_calc_155 = self.calculate_155(
            debtor_card.debt_value, _days, _percent, _share
        )
        debtor_card.update(peni_calc_155=_peni_calc_155).apply()

    async def check_peny(self):
        all_debtor = await DebtorCard.query.gino.all()
        debtor_cards = [self.peny_validate(debtor_card) for debtor_card in all_debtor]


async def connect():
    await db.set_bind('postgresql://{}:{}@{}/{}'.format(
        DATABASE["USERNAME"], DATABASE["PASSWORD"], DATABASE["HOST"], DATABASE["NAME"]
    ))

asyncio.get_event_loop().run_until_complete(connect())
