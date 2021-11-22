import logging

from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import timestamps
from test_cases.wrapper.eq_wrappers import *
from stubs import Stubs
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import call, get_base_request, close_fe
from test_cases.wrapper import eq_wrappers
from win_gui_modules.wrappers import verify_ent, verification
''' NOT DONE'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3826"
    seconds, nanos = timestamps()  # Store case start time
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "40"
    client = "MOClient"
    lookup = "VETO"
    order_type = "Limit"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    #  endregion
    # endregion
    # region create CO
    # bo_fields = {'0': 'BlockBO FIELD1', '1': 'BlockBO FIELD2', '2': 'BlockBO FIELD3', '3': 'BlockBO FIELD4',
    #              '4': 'BlockBO FIELD5'}
    # alloc_fields = {'0': 'AllocBO FIELD 1', '1': 'AllocBO FIELD 2', '2': 'AllocBO FIELD 3', '3': 'AllocBO FIELD 4',
    #                 '4': 'AllocBO FIELD 5'}
    # eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username,
    #                          price=price, misc_bo_fields=bo_fields, misc_alloc_fields=alloc_fields)
    # # endregion
    # scrolling_details = GridScrollingDetails(ScrollingOperation.UP, 3, base_request)
    # order_book_service = Stubs.win_act_order_book
    # call(order_book_service.orderBookGridScrolling, scrolling_details.build())
    # # region manual execute CO order
    # eq_wrappers.manual_execution(base_request, qty, price)
    # # endregion
    #
    # # region complete CO order
    # eq_wrappers.complete_order(base_request)
    # # endregion
    #
    # # region book Co order
    # eq_wrappers.book_order(base_request, client, agreed_price=price, misc_arr=["Changed BlockBO Field 1",
    #                                                                            "Changed BlockBO Field 2",
    #                                                                            "Changed BlockBO Field 3",
    #                                                                            "Changed BlockBO Field 4",
    #                                                                            "Changed BlockBO Field 5"])
    # middle_office_service = Stubs.win_act_middle_office_service
    # call(middle_office_service.middleOfficeGridScrolling, scrolling_details.build())
    # eq_wrappers.verify_block_value(base_request, case_id, 'Bo Field 1', 'Changed BlockBO Field 1')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Bo Field 2', 'Changed BlockBO Field 2')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Bo Field 3', 'Changed BlockBO Field 3')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Bo Field 4', 'Changed BlockBO Field 4')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Bo Field 5', 'Changed BlockBO Field 5')
    #
    # # endregion

    # region approve block
    # eq_wrappers.approve_block(base_request)
    # eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')
    # endregion

    # # region allocate CO order
    # param = [{"Security Account": "MOClient1_SA1", "Alloc Qty": qty}]
    # eq_wrappers.allocate_order(base_request, param)
    # eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')
    # eq_wrappers.verify_block_value(base_request, case_id, 'Summary Status', 'MatchedAgreed')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Status', 'Affirmed')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Match Status', 'Matched')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 1', 'AllocBO FIELD 1')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 2', 'AllocBO FIELD 2')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 3', 'AllocBO FIELD 3')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 4', 'AllocBO FIELD 4')
    # eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 5', 'AllocBO FIELD 5')
    # # endregion

    # region amend allocate
    eq_wrappers.amend_allocate(base_request, agreed_price=str(int(price) + 1),
                               misc_arr=['AllocBO FIELD 11', 'AllocBO FIELD 22', 'AllocBO FIELD 33',
                                         'AllocBO FIELD 44', 'AllocBO FIELD 55'])

    eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 1', 'AllocBO FIELD 11')
    eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 2', 'AllocBO FIELD 22')
    eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 3', 'AllocBO FIELD 33')
    eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 4', 'AllocBO FIELD 44')
    eq_wrappers.verify_allocate_value(base_request, case_id, 'Alloc BO Field 5', 'AllocBO FIELD 55')
    # endregion
