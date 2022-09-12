import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8253(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(self.fix_message)
        self.fix_cancel = FixMessageOrderCancelRequestOMS().set_default(self.fix_message)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # MOClient_PARIS
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        filter_list = [OrderBookColumns.order_id.value, order_id]
        # endregion
        # region Step 2
        self.order_book.mark_reviewed(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "Yes"})
        # endregion
        # region Step 3
        try:
            ocrr_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                    self.venue_client_name,
                                                                                    self.mic,
                                                                                    True)
            self.fix_cancel_replace.change_parameter("Price", str(int(self.price) + 1))
            self.fix_manager.send_message_fix_standard(self.fix_cancel_replace)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(ocrr_rule)
        self.order_book.refresh_order(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "No"})
        # endregion
        # region Step 4
        self.order_book.mark_reviewed(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "Yes"})
        # endregion
        # region Step 5
        try:
            ocr_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                            self.venue_client_name,
                                                                            self.mic,
                                                                            True)
            self.fix_manager.send_message_fix_standard(self.fix_cancel)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(ocr_rule)
        self.order_book.refresh_order(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "No"})
        # endregion
