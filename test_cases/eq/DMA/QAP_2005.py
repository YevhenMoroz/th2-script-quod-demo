import logging
import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import Connectivity
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_2005(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.qty = '500'
        self.price = '20'
        self.price_amend = '19'
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)

        self.fix_message_amend = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_message_cancel = FixMessageOrderCancelRequestOMS()

        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.exec_sts = None
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameter('Side', '2')
            self.fix_message.update_fields_in_component('OrderQtyData', {'OrderQty': self.qty})
            # self.fix_manager.send_message_fix_standard(self.fix_message)
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        # endregion
        # region Set-up parameters for ExecutionReports
        self.exec_report.set_default_new(self.fix_message)
        # self.exec_report.remove_parameter('Price')
        self.exec_report.change_parameters({'ReplyReceivedTime': '*', 'SecondaryOrderID': '*', 'Text': '*'})
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Check values in OrderBook
        sts = self.order_book.extract_field(OrderBookColumns.sts.value)
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.open.value},
                                       {OrderBookColumns.sts.value: sts}, 'Checking order status in the order book')
        # endregion

        print('-----------------------------------------AMEND Start----------------------')
        # region Amend order
        try:
            nos_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                   self.venue_client_names,
                                                                                   self.venue, True)
            self.fix_message_amend.set_default(self.fix_message)
            self.fix_message_amend.change_parameter('Price', self.price_amend)
            # response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_amend)
            self.fix_manager.send_message_fix_standard(self.fix_message_amend)
            # Front
            # self.order_ticket.set_order_details(limit='19')
            # self.order_ticket.amend_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        print('-----------------------------------------Cancel Start----------------------')
        # region Cancelling order
        try:
            nos_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                            self.venue_client_names,
                                                                            self.venue, True)
            self.fix_message_cancel.set_default(self.fix_message)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_cancel)
            # Front
            # self.order_book.cancel_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
