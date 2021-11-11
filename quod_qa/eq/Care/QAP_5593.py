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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5593"
    case_id = create_event(case_name, report_id)
    # region Declarations
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_window = BaseWindow(case_id, session_id)
    oms_order_book = OMSOrderBook(case_id, session_id)
    oms_order_inbox = OMSClientInbox(case_id, session_id)
    base_window.open_fe(session_id, report_id, work_dir, username, password)
    # # endregion
    fix_manager = FixManager('fix-sell-317-standard-test', case_id)
    fix_message_new_order_single = FixMessageNewOrderSingleOMS()
    fix_message_new_order_single.set_default_DMA(Instrument.ISI3)
    fix_message_new_order_single.change_parameters({"HandlInst": "3", "Account": "CLIENT_COMM_1", "Currency": "GBP"})
    fix_manager.send_message(fix_message_new_order_single)
    oms_order_inbox.accept_order('ISI3',
                                 fix_message_new_order_single.get_parameters().get('OrderQtyData').get('OrderQty'),
                                 fix_message_new_order_single.get_parameter("Price"))
    result = oms_order_book.manual_execution(
        fix_message_new_order_single.get_parameters().get('OrderQtyData').get('OrderQty'),
        fix_message_new_order_single.get_parameter("Price"),
        error_expected=True)
    expected_result = {'Trade Ticket Error': 'Error - [QUOD-11750] Manual execution requires Contra Firm'}
    oms_order_book.compare_values(expected_result, result, event_name='Check values')
