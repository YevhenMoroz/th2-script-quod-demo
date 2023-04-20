from datetime import datetime

from custom import basic_custom_actions 
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.base_data_set import BaseDataSet


class FixMessageNewOrderMultiLegAlgo(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.NewOrderMultiLeg.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_PairTrading_params(self) -> FixMessage:
        base_parameters = {
            'Account': self.get_data_set().get_client_by_name('client_2'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_41"),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrdType': '1',
            'OrderQty': '1000',
            'TimeInForce': '0',
            'PositionEffect': 'O',
            "OrderCapacity": "A",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'NoLegs': [
                {'InstrumentLeg': self.get_data_set().get_fix_leg_instrument_by_name("instrument_1")},
                {'InstrumentLeg': self.get_data_set().get_fix_leg_instrument_by_name("instrument_2")},
                ],
            'TargetStrategy': '1013',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'SpreadDeviationType',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'Currency'
                },
                {
                    'StrategyParameterName': 'SpreadDeviationNumber',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '5'
                },
                {
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '0.1'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self
