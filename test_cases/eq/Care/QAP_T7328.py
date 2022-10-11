import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7328(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client = self.fix_message.get_parameter('Account')
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)
        self.api_manager = RestApiManager(self.wa_connectivity, self.case_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.wash_book = self.rest_wash_book_message.default_washbook_account


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # endregion
        # region set up wash book rule
        self.rest_wash_book_message.modify_wash_book_rule(client=self.client)
        self.api_manager.send_post_request(self.rest_wash_book_message)
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        time.sleep(5)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.client_name.value: self.client,
             OrderBookColumns.washbook.value: self.wash_book})
        # endregion
