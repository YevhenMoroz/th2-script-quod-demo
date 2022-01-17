import logging
import os

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.base_window import BaseWindow
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5385"
    case_id = create_event(case_name, report_id)
    # region Declarations
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_window = BaseWindow(case_id, session_id)
    oms_order_book = OMSOrderBook(case_id, session_id)
    oms_order_inbox = OMSClientInbox(case_id, session_id)
    base_window.open_fe(session_id, report_id, work_dir, username, password)
    # endregion
    fix_manager = FixManager('fix-sell-317-standard-test', case_id)
    fix_message_new_order_single = FixMessageNewOrderSingleOMS()
    fix_message_new_order_single.set_default_care_limit(Instrument.ISI3)
    fix_message_new_order_single.change_parameters({"HandlInst": "3", "Account": "CLIENT_COMM_1", 'Currency': 'GBP',
                                                    "ExDestination": "XEUR"})
    fix_manager.send_message(fix_message_new_order_single)
    oms_order_book.scroll_order_book(1)
    qty = fix_message_new_order_single.get_parameters().get('OrderQtyData').get('OrderQty')
    oms_order_inbox.accept_order('VETO', qty, fix_message_new_order_single.get_parameter("Price"))
    oms_order_book.manual_execution(qty, fix_message_new_order_single.get_parameter("Price"), contra_firm='ContraFirm')
    oms_order_book.complete_order()
    order_id = oms_order_book.extract_field('Order ID')
    filter_for_extracting = {'Order ID': order_id}
    # endregion
    # region Extract value from Booking Ticket
    result_of_extraction = oms_order_book.extracting_values_from_booking_ticket([PanelForExtraction.COMMISSION],
                                                                                filter_for_extracting)

    result = BaseWindow.split_2lvl_values(result_of_extraction)
    expected_result = {'Basis': 'PerUnit', 'Rate': '0.01', 'Amount': '1', 'Currency': 'GBP'}
    oms_order_book.compare_values(expected_result, result[0], event_name='Check values')
