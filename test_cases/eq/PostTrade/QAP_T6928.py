import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.read_log_wrappers.ReadLogVerifier import ReadLogVerifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.read_log_wrappers.oms_messages.AlsMessages import AlsMessages
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, AllocationsColumns, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6928(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.als_email_report = self.environment.get_list_read_log_environment()[0].read_log_conn
        self.read_log_verifier = ReadLogVerifier(self.als_email_report, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.ord_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Variables
        client = self.data_set.get_client_by_name("client_pt_6")
        account1 = self.data_set.get_account_by_name("client_pt_6_acc_1")
        venue_client = self.data_set.get_venue_client_names_by_name("client_pt_6_venue_1")
        mic = self.data_set.get_mic_by_name("mic_1")
        # endregion
        # region Create care order
        change_params = {'Account': client}
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit().change_parameters(change_params)
        qty = nos.get_parameters()["OrderQtyData"]["OrderQty"]
        price = nos.get_parameters()["Price"]
        try:
            rule_manager = RuleManager(Simulators.equity)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       venue_client, mic,
                                                                                       int(price),
                                                                                       int(qty), 1)

            response = self.fix_manager.send_message_and_receive_response_fix_standard(nos)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(trade_rele)
        # endregion
        order_id = response[0].get_parameters()['OrderID']
        self.mid_office.book_order(filter=[OrderBookColumns.order_id.value, order_id])
        self.mid_office.override_confirmation_service(filter_dict={OrderBookColumns.order_id.value: order_id})
        self.mid_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: account1, AllocationsColumns.alloc_qty.value: qty}]
        self.mid_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.mid_office.allocate_block(filter=[MiddleOfficeColumns.order_id.value, order_id])
        # region Check ALS logs Status New
        als_message = AlsMessages.execution_report.value
        als_message.update({"ConfirmStatus": "New", "ClientAccountID": account1})
        self.read_log_verifier.check_read_log_message(als_message, ["ClientAccountID"], timeout=60000)
        # endregion
