import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6929(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client_new = self.data_set.get_client_by_name("client_pt_1")
        self.client = self.data_set.get_client_by_name("client_dummy")
        self.client_acc = self.data_set.get_account_by_name("client_pt_1_acc_1")
        self.venue_cl_acc = self.data_set.get_venue_client_account('client_pt_1_acc_1_venue_client_account')
        self.change_params = {'Account': self.client}
        self.fix_message.change_parameters(self.change_params)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # endregion
        # region group modify
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).group_modify(self.client_new, security_account=self.client_acc)
        # endregion
        # region Check VenueClientAccount field
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.venue_client_account.value: self.venue_cl_acc})
        # endregion
