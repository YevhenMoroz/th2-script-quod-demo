import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.order_book_wrappers import ManualExecutingDetails
from win_gui_modules.order_book_wrappers import CompleteOrdersDetails
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.wrappers import *
from rule_management import RuleManager

#from test_cases.QAP_1560 import TestCase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    rule_manager = RuleManager()

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-3338"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    session_id = set_session_id()
    #set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        qty = "300"
        limit = "10"
        lookup = "VETO"
        today = datetime.now()
        todayp2 = today + timedelta(days=2)
        todayp2 = todayp2.strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')

        # Checkpoint1 creation
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint

        #create care order
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client("MOClient")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user_305'], True)

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)

        set_base(session_id, case_id)

        order_ticket_service = Stubs.win_act_order_ticket
        order_book_service = Stubs.win_act_order_book
        common_act = Stubs.win_act

        call(order_ticket_service.placeOrder, new_order_details.build())

        order_info_extraction = "getOrderInfo"

        data = call(common_act.getOrderFields, fields_request(order_info_extraction,
                                                             ["order.status", "Sts", "order.order_id", "Order ID"]))
        care_order_id = data["order.order_id"]
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))

        #verify execution report
        execution_report1_params = {
            'ClOrdID': care_order_id,
            'OrderID': care_order_id,
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'SettlDate': todayp2,

            'OrderQtyData': {
                'OrderQty': qty
            },
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'VETO',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'OrdType': '2',
            'Side': '1',
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '0',
            'LeavesQty': qty,
            'Price': limit,
            'TimeInForce': '0'
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report1_params, ['OrderID']),
                checkpoint_id1, 'fix-ss-back-office', case_id
            )
        )

        # Checkpoint2 creation
        checkpoint_response2 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id2 = checkpoint_response2.checkpoint

        #create manual execution
        service = Stubs.win_act_order_book

        manual_executing_details = ManualExecutingDetails(base_request)
        manual_executing_details.set_filter({"Order ID": care_order_id})
        # manual_executing_details.set_row_number(1)

        executions_details = manual_executing_details.add_executions_details()
        #executions_details.set_quantity(qty)
        #executions_details.set_price(limit)
        executions_details.set_executing_firm("ExecutingFirm")
        executions_details.set_contra_firm("Contra_Firm")
        executions_details.set_last_capacity("Agency")

        call(service.manualExecution, manual_executing_details.build())

        #verify execution report2
        execution_report2_params = {
            'ClOrdID': care_order_id,
            'OrderID': care_order_id,
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': qty,
            'Price': limit,
            'SettlDate': todayp2,
            'OrderQtyData': {
                'OrderQty': qty
            },
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'VETO',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'OrdType': '2',
            'Side': '1',
            'AvgPx': limit,
            'OrdStatus': '2',
            'ExecType': 'F',
            'LeavesQty': '0',
            'TimeInForce': '0',
            'TradeDate': today
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report2_params, ['OrderID']),
                checkpoint_id2, 'fix-ss-back-office', case_id
            )
        )

        #complete order
        #service = Stubs.win_act_order_book

        complete_orders_details = CompleteOrdersDetails(base_request)
        complete_orders_details.set_filter({"Order ID": care_order_id})
        # complete_orders_details.set_selected_row_count(2)

        call(service.completeOrders, complete_orders_details.build())

        # Checkpoint3 creation
        checkpoint_response3 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id3 = checkpoint_response3.checkpoint

        #book order
        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["Order ID", care_order_id])
        # modify_request.set_selected_row_count(4)

        misc_details = modify_request.add_misc_details()
        misc_details.set_bo_field_1("BOF1C")
        misc_details.set_bo_field_2("BOF2C")
        misc_details.set_bo_field_3("BOF3C")
        misc_details.set_bo_field_4("BOF4C")
        misc_details.set_bo_field_5("BOF5C")

        extraction_details = modify_request.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_net_price("book.netPrice")
        extraction_details.extract_net_amount("book.netAmount")
        extraction_details.extract_total_comm("book.totalComm")
        extraction_details.extract_gross_amount("book.grossAmount")
        extraction_details.extract_total_fees("book.totalFees")
        extraction_details.extract_agreed_price("book.agreedPrice")

        call(middle_office_service.bookOrder, modify_request.build())

        #approve
        #middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["Order ID", care_order_id])
        call(middle_office_service.approveMiddleOfficeTicket, modify_request.build())

        #verify allocationinstruction 1
        allocation_instruction_report1_params = {
            'TransactTime': '*',
            'Side': '1',
            'AvgPx': limit,
            'Currency': 'EUR',
            'Quantity': qty,
            'SettlDate': today,
            'AllocID': '*',
            'TradeDate': today,
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'FR0004186856_EUR',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'NoParty': [
                {
                    'PartyRole': '17',
                    'PartyID': 'Contra_Firm',
                    'PartyIDSource': 'N',

                },
                {
                    'PartyRole': '1',
                    'PartyID': 'ExecutingFirm',
                    'PartyIDSource': 'N',
                }
            ],
            'AllocInstructionMiscBlock1': {
                'BOMiscField0': 'BOF1C',
                'BOMiscField1': 'BOF2C',
                'BOMiscField2': 'BOF3C',
                'BOMiscField3': 'BOF4C',
                'BOMiscField4': 'BOF5C'
            },
            'NoOrders': [{
                'OrderID': care_order_id,
                'ClOrdID': care_order_id
            }],
            'AllocType': 5,
            'AllocTransType': 2,
        }
        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Allocation Instruction Report",
                bca.filter_to_grpc_nfu("AllocationInstruction", allocation_instruction_report1_params, ['OrderID',
                                                                                                        'AllocType']),
                checkpoint_id3, 'fix-ss-back-office', case_id
            )
        )

        # Checkpoint4 creation
        checkpoint_response4 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id4 = checkpoint_response4.checkpoint

        #allocate
        #middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        allocations_details = modify_request.add_allocations_details()
        allocations_details.add_allocation_param({"Security Account": "MOClientSA1", "Alloc Qty": '100',
                                                  "BO Field 1": "BOF1A1", "BO Field 2": "BOF2A1",
                                                  "BO Field 3": "BOF3A1", "BO Field 4": "BOF4A1",
                                                  "BO Field 5": "BOF5A1"})
        allocations_details.add_allocation_param({"Security Account": "MOClientSA2", "Alloc Qty": '200',
                                                  "BO Field 1": "BOF1A2", "BO Field 2": "BOF2A2",
                                                  "BO Field 3": "BOF3A2", "BO Field 4": "BOF4A2",
                                                  "BO Field 5": "BOF5A2"})

        extraction_details = modify_request.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_net_price("book.netPrice")
        extraction_details.extract_net_amount("book.netAmount")
        extraction_details.extract_total_comm("book.totalComm")
        extraction_details.extract_gross_amount("book.grossAmount")
        extraction_details.extract_total_fees("book.totalFees")
        extraction_details.extract_agreed_price("book.agreedPrice")

        call(middle_office_service.allocateMiddleOfficeTicket, modify_request.build())

        #verify confirmation1
        confirmation_report_params1 = {
            'TransactTime': '*',
            'AllocAccount': 'MOClientSA1',
            'ConfirmType': '*',
            'SettlDate': today,
            'AllocID': '*',
            'TradeDate': today,
            'ConfirmID': '*',
            'AllocQty': '100',
            'MatchStatus': '0',
            'ConfirmStatus': '1',
            'Currency': 'EUR',
            'Side': '1',
            'AvgPx': limit,
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'FR0004186856_EUR',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'NoParty': [
                {
                    'PartyRole': '17',
                    'PartyID': 'Contra_Firm',
                    'PartyIDSource': 'N',

                },
                {
                    'PartyRole': '1',
                    'PartyID': 'ExecutingFirm',
                    'PartyIDSource': 'N',
                }
            ],
            'NoOrders': [{
                'OrderID': care_order_id,
                'ClOrdID': care_order_id
            }],
            'AllocInstructionMiscBlock2': {
                'BOMiscField5': 'BOF1A1',
                'BOMiscField6': 'BOF2A1',
                'BOMiscField7': 'BOF3A1',
                'BOMiscField8': 'BOF4A1',
                'BOMiscField9': 'BOF5A1'
            },
            'AllocInstructionMiscBlock1': {
                'BOMiscField0': 'BOF1C',
                'BOMiscField1': 'BOF2C',
                'BOMiscField2': 'BOF3C',
                'BOMiscField3': 'BOF4C',
                'BOMiscField4': 'BOF5C'
            },
            'ConfirmTransType': 2,
        }
        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Confirmation Report",
                bca.filter_to_grpc_nfu("Confirmation", confirmation_report_params1, ['OrderID', 'AllocAccount']),
                checkpoint_id4, 'fix-ss-back-office', case_id
            )
        )

        #verify confirmation
        confirmation_report_params2 = {
            'TransactTime': '*',
            'AllocAccount': 'MOClientSA2',
            'ConfirmType': '*',
            'SettlDate': today,
            'AllocID': '*',
            'TradeDate': today,
            'ConfirmID': '*',
            'AllocQty': '200',
            'MatchStatus': '0',
            'ConfirmStatus': '1',
            'Currency': 'EUR',
            'Side': '1',
            'AvgPx': limit,
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'FR0004186856_EUR',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'NoParty': [
                {
                    'PartyRole': '17',
                    'PartyID': 'Contra_Firm',
                    'PartyIDSource': 'N',

                },
                {
                    'PartyRole': '1',
                    'PartyID': 'ExecutingFirm',
                    'PartyIDSource': 'N',
                }
            ],
            'NoOrders': [{
                'OrderID': care_order_id,
                'ClOrdID': care_order_id
            }],
            'AllocInstructionMiscBlock2': {
                'BOMiscField5': 'BOF1A2',
                'BOMiscField6': 'BOF2A2',
                'BOMiscField7': 'BOF3A2',
                'BOMiscField8': 'BOF4A2',
                'BOMiscField9': 'BOF5A2'
            },
            'AllocInstructionMiscBlock1': [{
                'BOMiscField0': 'BOF1C',
                'BOMiscField1': 'BOF2C',
                'BOMiscField2': 'BOF3C',
                'BOMiscField3': 'BOF4C',
                'BOMiscField4': 'BOF5C'
            }],
            'ConfirmTransType': 2,
        }
        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Confirmation Report",
                bca.filter_to_grpc_nfu("Confirmation", confirmation_report_params2, ['OrderID', 'AllocAccount']),
                checkpoint_id4, 'fix-ss-back-office', case_id
            )
        )

        #verify allocationinstruction2
        allocation_instruction_report2_params = {
            'TransactTime': '*',
            'Side': '1',
            'AvgPx': limit,
            'Currency': 'EUR',
            'Quantity': qty,
            'SettlDate': today,
            'AllocID': '*',
            'TradeDate': today,
            'Instrument': {
                'SecurityDesc': 'VETOQUINOL',
                'Symbol': 'FR0004186856_EUR',
                'SecurityIDSource': '4',
                'SecurityID': 'FR0004186856',
                'SecurityExchange': 'XPAR',

            },
            'NoParty': [
                {
                    'PartyRole': '17',
                    'PartyID': 'Contra_Firm',
                    'PartyIDSource': 'N',

                },
                {
                    'PartyRole': '1',
                    'PartyID': 'ExecutingFirm',
                    'PartyIDSource': 'N',
                }
            ],
            'NoAllocs': [
                {
                    'AllocQty': '100',
                    'AllocAccount': 'MOClientSA1',
                    'AllocInstructionMiscBlock2': {
                        'BOMiscField5': 'BOF1A1',
                        'BOMiscField6': 'BOF2A1',
                        'BOMiscField7': 'BOF3A1',
                        'BOMiscField8': 'BOF4A1',
                        'BOMiscField9': 'BOF5A1'
                    }
                },
                {
                    'AllocQty': '200',
                    'AllocAccount': 'MOClientSA2',
                    'AllocInstructionMiscBlock2': {
                        'BOMiscField5': 'BOF1A2',
                        'BOMiscField6': 'BOF2A2',
                        'BOMiscField7': 'BOF3A2',
                        'BOMiscField8': 'BOF4A2',
                        'BOMiscField9': 'BOF5A2'
                    }
                }
            ],
            'AllocInstructionMiscBlock1': {
                'BOMiscField0': 'BOF1C',
                'BOMiscField1': 'BOF2C',
                'BOMiscField2': 'BOF3C',
                'BOMiscField3': 'BOF4C',
                'BOMiscField4': 'BOF5C'
            },
            'NoOrders': [{
                'OrderID': care_order_id,
                'ClOrdID': care_order_id
            }],
            'AllocType': 2,
            'AllocTransType': 2,
        }
        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Allocation Instruction Report",
                bca.filter_to_grpc_nfu("AllocationInstruction", allocation_instruction_report2_params, ['OrderID',
                                                                                                        'AllocType']),
                checkpoint_id4, 'fix-ss-back-office', case_id
            )
        )
    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
