import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7019(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.oms_basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.str_name = 'Urgency'
        self.ex_str_name = '14'
        self.params = {
            "TargetStrategy": "1021",
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order with algo param
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region recieve message
        self.execution_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report1)
        # endregion
        # region check message
        fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(self.fix_message)
        fix_message_cancel_replace.add_tag(self.params)
        self.fix_manager.send_message_and_receive_response_fix_standard(fix_message_cancel_replace)
        # endregion
        # region accept modify
        self.client_inbox.accept_modify_plus_child()
        # endregion
        # region accept modify
        self.execution_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_replaced(self.fix_message)
        self.execution_report2.add_tag(self.params)
        self.execution_report2.change_parameters({ "OrigClOrdID":"*", "SettlDate":"*", "SettlType":"B"})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report2)
        # endregion