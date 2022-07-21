import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
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


class QAP_2008(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.qty_amend = '700'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_amend = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_message_cancel = FixMessageOrderCancelRequestOMS()
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.sts = None
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.future_date = datetime.now() + timedelta(days=2)
        self.expire_date = datetime.strftime(self.future_date, "%Y%m%d")
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
            self.fix_message.change_parameters({'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'TimeInForce': '6',
                                                'ExpireDate': self.expire_date})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Order ID
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Set-up parameters for ExecutionReports
        self.exec_report.set_default_new(self.fix_message)

        # Depends on Weekend Day settings on Venue
        # if self.future_date.isoweekday() == 6:
        #     self.expire_date = datetime.strftime(self.future_date - timedelta(days=1), "%Y%m%d")
        # elif self.future_date.isoweekday() == 7:
        #     self.expire_date = datetime.strftime(self.future_date - timedelta(days=2), "%Y%m%d")
        self.exec_report.change_parameters(
            {'ReplyReceivedTime': '*', 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             'ExpireDate': self.expire_date})
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Check values in OrderBook
        self.sts = self.order_book.extract_field(OrderBookColumns.sts.value)
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.open.value},
                                       {OrderBookColumns.sts.value: self.sts},
                                       'Checking order status in the Order book')
        # endregion

        # region Amend order
        try:
            nos_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                   self.venue_client_names,
                                                                                   self.venue, True)
            # FIX
            # self.fix_message_amend.set_default(self.fix_message)
            # self.fix_message_amend.update_fields_in_component('OrderQtyData', {'OrderQty': self.qty_amend})
            # response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_amend)

            # Front
            self.order_ticket.set_order_details(qty=self.qty_amend)
            self.order_ticket.amend_order([OrderBookColumns.order_id.value, order_id])
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Check values in OrderBook after Amend
        qty_after_amend = self.order_book.extract_field(OrderBookColumns.qty.value)
        self.order_book.compare_values({OrderBookColumns.qty.value: self.qty_amend},
                                       {OrderBookColumns.qty.value: qty_after_amend},
                                       'Checking the Qty after amending in the Order book')
        # endregion

        # region Cancelling order
        try:
            nos_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                            self.venue_client_names,
                                                                            self.venue, True)
            self.fix_message_cancel.set_default(self.fix_message)
            self.fix_manager.send_message_fix_standard(self.fix_message_cancel)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Check values in OrderBook after Cancel
        self.sts = self.order_book.extract_field(OrderBookColumns.sts.value)
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.cancelled.value},
                                       {OrderBookColumns.sts.value: self.sts},
                                       'Checking order status after cancelling in the Order book')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
