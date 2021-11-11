import logging
import os
import time

from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from quod_qa.wrapper_test.DataSet import Connectivity
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5881"
    qty = "100"
    price = "10"
    client = "CLIENT_COMM_1"
    case_id = create_event(case_name, report_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    middle_office = OMSMiddleOfficeBook(case_id, session_id)
    middle_office.open_fe(session_id, report_id, case_id, work_dir, username, password)
    no_allocs: dict = {"NoAllocs": [{
        'AllocAccount': "CLIENT_COMM_1_SA4",
        'AllocQty': qty
    }]}
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(Connectivity.Ganymede_317_buy.value,
                                                                             client + '_PARIS', "XPAR", float(price))
        fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, report_id)
        new_order_single1 = FixMessageNewOrderSingleOMS().set_default_DMA().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs})
        new_order_single2 = FixMessageNewOrderSingleOMS().set_default_DMA().add_ClordId(
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
    middle_office.set_modify_ticket_details(is_alloc_amend=True, comm_rate="1.555", toggle_manual=True,
                                            remove_comm=True,
                                            comm_basis="Absolute")
    middle_office.amend_allocate()
    expected_value = middle_office.extract_allocate_value("Client Comm")
    middle_office.compare_values({"Client Comm": "1.555"}, expected_value,
                                 event_name='Compare commissions')
