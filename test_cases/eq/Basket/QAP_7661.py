import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsRoutes
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, BasketBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_7661(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.oms_basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.str_name = 'Urgency'
        self.ex_str_name = '14'
        self.params1 = {
            "Account": self.data_set.get_client_by_name("client_co_1"),
            "HandlInst": "3",
            "Side": "1",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_co_1_acc_1"),
                                          'AllocQty': "100"}]},
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_1"),
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": data_set.get_currency_by_name("currency_1"),
            "TargetStrategy": "1021",  # 2021 = TWAP_ASIA
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.params2 = {
            "Account": self.data_set.get_client_by_name("client_co_1"),
            "HandlInst": "3",
            "Side": "2",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "2",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.data_set.get_account_by_name("client_co_1_acc_1"),
                                          'AllocQty': "100"}]},
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_1"),
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": self.data_set.get_currency_by_name("currency_1"),
            "TargetStrategy": "1021",  # 2021 = TWAP_ASIA
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.fix_message.change_parameter('ListOrdGrp', {'NoOrders': [self.params1, self.params2]})
        self.route = OmsRoutes.route_1.value


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket
        self.fix_manager.send_message_fix_standard(self.fix_message)
        basket_id = self.oms_basket_book.get_basket_value(BasketBookColumns.id.value)
        # endregion
        # region accept CO orders
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region wave basket
        self.oms_basket_book.wave_basket(route=self.route)
        # endregion
        # region check value
        self.oms_basket_book.check_basket_sub_lvl_field(1, BasketBookColumns.status_wave.value, BasketBookColumns.waves_tab.value, ExecSts.new.value)
        # endregion
