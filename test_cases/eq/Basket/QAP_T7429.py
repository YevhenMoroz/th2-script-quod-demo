import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7429(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_manager.send_message_fix_standard(nol)
        client_basket_id = nol.get_parameters()['ListID']
        # endregion
        # region Set-up parameters for ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(nol)
        # endregion
        # region Check ListStatus
        self.fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region cancel Basket
        self.basket_book.cancel_basket({BasketBookColumns.client_basket_id.value: client_basket_id})
        # endregion
        # region check cancelled Basket sts
        self.basket_book.check_basket_field(BasketBookColumns.status.value, BasketBookColumns.canceling.value)
        # endregion
        # region accept cancel
        self.client_inbox.accept_and_cancel_children()
        self.client_inbox.accept_and_cancel_children()
        # endregion
        # region check all done Basket sts and orders cancelled sts
        self.basket_book.check_basket_field(BasketBookColumns.status.value, BasketBookColumns.all_done.value)
        self.basket_book.check_basket_sub_lvl_field(1, BasketBookColumns.orders_sts.value,
                                                    BasketBookColumns.orders_tab.value, ExecSts.cancelled.value)
        self.basket_book.check_basket_sub_lvl_field(2, BasketBookColumns.orders_sts.value,
                                                    BasketBookColumns.orders_tab.value, ExecSts.cancelled.value)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled_list(nol)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled_list(nol, 1)
        exec_report1.add_tag({"SettlDate": "*", "ExpireDate": "*", "CxlQty": "*"})
        exec_report1.remove_parameter("OrigClOrdID")
        exec_report2.add_tag({"SettlDate": "*", "ExpireDate": "*", "CxlQty": "*"})
        exec_report2.remove_parameter("OrigClOrdID")
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message(exec_report1)
        self.fix_verifier.check_fix_message(exec_report2)
        # endregion
