import logging
import os
import time

from custom.basic_custom_actions import create_event
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5859"
    qty = "100"
    price = "10"
    client = "CLIENT_COMM_1"
    case_id = create_event(case_name, report_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    middle_office = OMSMiddleOfficeBook(case_id, session_id)
    middle_office.open_fe(session_id, report_id, case_id, work_dir, username, password)
    no_allocs: dict = {"NoAllocs": [{'AllocAccount': "CLIENT_COMM_1_SA4", 'AllocQty': str(int(qty) / 2)},
                                    {'AllocAccount': "CLIENT_COMM_1_SA5", 'AllocQty': str(int(qty) / 2)}]}
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(Connectivity.Ganymede_317_bs.value,
                                                                             client + '_PARIS', "XPAR", float(price))
        fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, report_id)
        new_order_single1 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs})
        new_order_single2 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs,
             "Side": "2"})
        fix_manager.send_message_and_receive_response(new_order_single1)
        fix_manager.send_message_and_receive_response(new_order_single2)
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)

    middle_office.book_order()
    middle_office.approve_block()
    middle_office.allocate_block()
    expected_value1 = middle_office.extract_allocate_value("Client Comm", account="CLIENT_COMM_1_SA5")
    middle_office.compare_values({"Client Comm": "100"}, expected_value1,
                                 event_name='Compare commissions')
    expected_value2 = middle_office.extract_allocate_value("Client Comm", account="CLIENT_COMM_1_SA4")
    middle_office.compare_values({"Client Comm": "1.123"}, expected_value2,
                                 event_name='Compare commissions')
