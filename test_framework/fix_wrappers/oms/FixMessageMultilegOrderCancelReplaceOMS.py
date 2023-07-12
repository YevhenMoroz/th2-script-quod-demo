from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.base_data_set import BaseDataSet


class FixMessageMultilegOrderCancelReplaceOMS(FixMessage):

    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.MultilegOrderCancelReplace.value, data_set=data_set)
        super().change_parameters(parameters)
        self.base_parameters = {
            'Account': self.get_data_set().get_client_by_name('client_1'),
            'HandlInst': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_multileg_paris"),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrdType': '1',
            'OrderQtyData': {'OrderQty': '100'},
            'TimeInForce': '0',
            'Price': '20',
            'PositionEffect': 'O',
            "OrderCapacity": "A",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'LegOrdGrp': {'NoLegs': [
                {'InstrumentLeg': self.get_data_set().get_fix_leg_instrument_by_name(
                    "instrument_multileg_paris_leg_1")},
                {'LegRatioQty': '1', 'LegSide': '1'},
                {'InstrumentLeg': self.get_data_set().get_fix_leg_instrument_by_name(
                    "instrument_multileg_paris_leg_2")},
                {'LegRatioQty': '1', 'LegSide': '2'},
            ]},
        }

    def set_default(self, new_order_multileg: dict):
        self.change_parameters(self.base_parameters)
        self.change_parameters({
            'ClOrdID': new_order_multileg['ClOrdID'],
            'OrigClOrdID': new_order_multileg['ClOrdID'],
            'TransactTime': datetime.utcnow().isoformat()
        })
        return self
