import asyncio
from gino import Gino

from local_settings import DATABASE


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
    payment_by_receipt = db.Column()
    debt_calculation = db.Column()
    peni_calc_155 = db.Column()
    peni_calc_395 = db.Column()
    state_fees_calc = db.Column()
    debt_data = db.Column()
    validation = db.Column()


class BaseLogic:
    async def check(self):  # TODO write logic
        pass


async def connect():
    await db.set_bind('postgresql://{}:{}@{}/{}'.format(
        DATABASE["USERNAME"], DATABASE["PASSWORD"], DATABASE["HOST"], DATABASE["NAME"]
    ))

asyncio.get_event_loop().run_until_complete(connect())
