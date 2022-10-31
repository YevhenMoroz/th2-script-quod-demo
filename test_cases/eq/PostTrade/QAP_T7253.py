import logging
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7253(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.booking_win = OMSBookingWindow(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = os.path.abspath("th2-script-quod-demo\\test_framework\ssh_wrappers\oms_cfg_files\client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create Care order via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Price': self.price, "TimeInForce": "1", 'OrderQtyData': {'OrderQty': self.qty},
             'Account': self.client})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        # endregion
        ord_filter = {OrderBookColumns.order_id.value: order_id}
        self.cl_inbox.accept_order(filter=ord_filter)
        exec_qty = str(int(int(self.qty) / 2))
        self.order_book.manual_execution(exec_qty, filter_dict=ord_filter)
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        # region Check values in OrderBook
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion
        # region Book order and checking values after it in the Order book
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        match_status = self.middle_office.extract_block_field(MiddleOfficeColumns.match_status.value,
                                                              [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.match_status.value: 'Unmatched'}, match_status,
            'Comparing values after Book for block of MiddleOffice')
        # endregion
        # region Setup ORS config
        tree = ET.parse(self.local_path)
        now = datetime.now(timezone.utc) + timedelta(minutes=1)
        schedule_time = now.strftime("%H:%M")
        element = ET.fromstring(f"<uncomplete><nonforex><scheduled>true</scheduled><zone>UTC</zone><at>{schedule_time}</at></nonforex></uncomplete>")
        ors = tree.getroot().find("ors")
        ors.append(element)
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")

        # endregion
        # region Check Order
        time.sleep(60)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.post_trade_status.value:
                                                     PostTradeStatuses.ready_to_book.value},
                                                'Comparing values after auto uncomplete',
                                                verification_method=VerificationMethod.NOT_EQUALS)
        # endregion
        self.order_book.manual_execution(filter_dict=ord_filter)
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])

        # region Book order and checking values after it in the Order book
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        match_status = self.middle_office.extract_block_field(MiddleOfficeColumns.match_status.value,
                                                              [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.match_status.value: 'Unmatched'}, match_status,
            'Comparing match_status after Book for 1st block of MiddleOffice')
        book_qty = self.middle_office.extract_block_field(MiddleOfficeColumns.qty.value,
                                                              [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.qty.value: exec_qty}, book_qty,
            'Comparing qty after Book for 2nd block of MiddleOffice')
        # endregion
        # region Cancel Booking and check
        self.booking_win.cancel_booking({MiddleOfficeColumns.order_id.value: order_id})
        status = self.middle_office.extract_block_field(MiddleOfficeColumns.sts.value,
                                                              [MiddleOfficeColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'Canceled'}, status,
            'Comparing status after Book for block of MiddleOffice')
        # endregion

        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.qty.value: exec_qty}, book_qty,
            'Comparing qty after Book for 3st block of MiddleOffice')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
