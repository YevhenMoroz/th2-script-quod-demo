import logging
import os
import time

from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.DataSet import Connectivity
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5926"
    qty = "100"
    price = "10"
    client = "CLIENT_COMM_1"
    case_id = create_event(case_name, report_id)
    middle_office = OMSMiddleOfficeBook(case_id, session_id)
    order_book = OMSOrderBook(case_id, session_id)
    __open_front_end(case_id, middle_office, report_id, session_id)
    __send_fix_orders(client, price, qty, report_id)

    middle_office.mass_book([1, 2])
    after_book_data = {"PostTradeStatus": "Booked"}
    __verify_data(after_book_data, order_book)
    middle_office.mass_un_book([1, 2])
    after_unbook_data = {"PostTradeStatus": "ReadyToBook"}
    order_book.set_order_details()
    __verify_data(after_unbook_data, order_book)


def __open_front_end(case_id, middle_office, report_id, session_id):
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    middle_office.open_fe(session_id, report_id, case_id, work_dir, username, password)


def __send_fix_orders(client, price, qty, report_id):
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
            Connectivity.Ganymede_317_bs.value, client + '_PARIS', "XPAR", float(price), float(price), int(qty),
            int(qty), 1)
        fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, report_id)
        new_order_single1 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client})
        new_order_single2 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, "Side": "2"})
        fix_manager.send_message_and_receive_response(new_order_single1)
        fix_manager.send_message_and_receive_response(new_order_single2)
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)


def __verify_data(verification_data, order_book):
    actual_after_unbook_data1 = order_book.extract_fields_list(verification_data, 1)
    order_book.compare_values(verification_data, actual_after_unbook_data1,
                              event_name='Check values')
    order_book.set_order_details()
    actual_after_unbook_data2 = order_book.extract_fields_list(verification_data, 2)
    order_book.compare_values(verification_data, actual_after_unbook_data2,
                              event_name='Check values')
