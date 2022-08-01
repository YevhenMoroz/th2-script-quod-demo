import logging
import time
from datetime import datetime
from pathlib import Path

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, ExecSts, \
    SecondLevelTabs, DoneForDays, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6983(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client('client_pt_1')
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.act_java_api = Stubs.act_java_api
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1)
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        middle_office_filter = [MiddleOfficeColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        # endregion

        # region check expected result from step 1
        self.order_book.set_filter(filter_list)
        actually_result = self.order_book.extract_fields_list({OrderBookColumns.sts.value: OrderBookColumns.sts.value})
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.open.value}, actually_result,
                                       f'Comparing Sts value of {order_id}')
        # endregion

        # region step 2 and step 3
        self.__split_co_order(qty=str(int(int(self.qty) / 2)), price=self.price, filter_list=filter_list)
        # endregion

        # region check expected_result of step 3
        actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value,
                                                               OrderBookColumns.order_id.value], [1], filter_dict)[0]
        print(actually_result)
        child_order_id = actually_result.pop('ID')
        expected_result = {OrderBookColumns.sts.value: ExecSts.terminated.value}

        self.order_book.compare_values(expected_result, actually_result, 'Comparing status of child order from step 3')
        # endregion

        # region step 4
        self.order_book.manual_execution(filter_dict=filter_dict)
        # endregion

        # region check expected result from step 4
        self.__comparing_values_in_order_book({OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value},
                                              {OrderBookColumns.exec_sts.value: ExecSts.filled.value}, filter_list,
                                              f'Comparing {OrderBookColumns.exec_sts.value} value of {order_id}')
        # endregion

        # region step 5
        self.order_book.complete_order(filter_list=filter_list)
        self.middle_office.book_order(filter_list)
        # endregion

        # region check expected result from step 5
        values = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value,
                                                                  MiddleOfficeColumns.match_status.value],
                                                                 filter_list=middle_office_filter)
        expected_result = {MiddleOfficeColumns.sts.value: MiddleOfficeColumns.appr_pending_sts.value,
                           MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.unmatched_sts.value}
        self.middle_office.compare_values(expected_result, values, f'Comparing values block of {order_id} from step 5')
        self.__comparing_values_in_order_book({OrderBookColumns.done_for_day.value: OrderBookColumns.done_for_day.value,
                                               OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value},
                                              {OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
                                               OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
                                              filter_list,
                                              f'Comparing values of {order_id} after book from step 5')
        # endregion

        # region step 6
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            "Header": {
                "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            },
            "OrdReportBlock": {
                "LastVenueOrdID": "*",
                "ClOrdID": child_order_id,
                "ReplySource": "Exchange",
                "TransactTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "FreeNotes": "reportViaJavaApi",
                "Side": "Buy",
                "OrdQty": str(int(int(self.qty) / 2)),
                "Price": self.price,
                "VenueExecID": "2",
                "CumQty": str(int(int(self.qty) / 2)),
                "LeavesQty": "0.0",
                "AvgPrice": self.price,
                "ExecType": "Eliminated",
                "ReplyReceivedTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            }
        }
        order_report = OrdReportOMS(parameters=base_parameters, data_set=self.data_set)
        self.java_api_manager.send_message(order_report)
        # endregion

        # region check expected result from step 6
        values = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value,
                                                                  MiddleOfficeColumns.match_status.value],
                                                                 filter_list=middle_office_filter)
        expected_result = {MiddleOfficeColumns.sts.value: MiddleOfficeColumns.appr_pending_sts.value,
                           MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.unmatched_sts.value}
        self.middle_office.compare_values(expected_result, values, f'Comparing values block of {order_id} from step 6')
        self.__comparing_values_in_order_book({OrderBookColumns.done_for_day.value: OrderBookColumns.done_for_day.value,
                                               OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value},
                                              {OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
                                               OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
                                              filter_list,
                                              f'Comparing  values of {order_id} from 6 step')

        actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value,
                                                               OrderBookColumns.order_id.value], [1], filter_dict)[0]
        expected_result = {OrderBookColumns.sts.value: ExecSts.eliminated.value}
        self.order_book.compare_values(expected_result, actually_result, 'Comparing status of child order from step 6')
        # endregion

    def __split_co_order(self, qty: str, price: str, filter_list: list):
        new_order_rule = trade_rule = None
        venue = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        try:
            new_order_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, client, venue, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client, venue, float(price),
                                                                                            int(qty), delay=0
                                                                                            )
            self.order_ticket.set_order_details(qty=qty, limit=price)
            self.order_ticket.split_order(filter_list)
        except Exception as e:
            logger.error(f"{e}", exc_info=True, stack_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_rule)
            self.rule_manager.remove_rule(trade_rule)

    def __comparing_values_in_order_book(self, list_of_column: dict, expected_result, filter_list: list, message):
        self.order_book.set_filter(filter_list)
        actually_result = self.order_book.extract_fields_list(list_of_column)
        self.order_book.compare_values(expected_result, actually_result,
                                       f'{message}')
