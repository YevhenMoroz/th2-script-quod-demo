import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from schemas import send_and_cancel, send_and_amend
import grpc
import copy

from grpc_modules import act_fix_pb2
from grpc_modules import act_fix_pb2_grpc
from grpc_modules import event_store_pb2
from grpc_modules import event_store_pb2_grpc
from grpc_modules import infra_pb2
from grpc_modules import verifier_pb2
from grpc_modules import verifier_pb2_grpc

timeouts = False
# TH2 components adresses
ACT = '10.0.22.22:30774'
VERIFIER = '10.0.22.22:32082'
EVENT_STORAGE = '10.0.22.22:31413'


def execute(case_name, report_id, case_params):
    seconds, nanos = bca.timestamps()  # Store case start time

    # Prepare user input
    new_order_single_1_params = {
        'ClOrdID': bca.client_orderid(9),
        # 'Parties': "",
        'Account': "KEPLER",
        'HandlInst': '2',
        'Instrument': case_params['Instrument'],
        'Side': case_params['Side_ord1'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': case_params['OrderQty_ord1'],
        'OrdType': '2',
        'Price': case_params['Price_ord1']
    }
    enter_order_1 = bca.act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder ord1',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_single_1_params)
        ))

    execution_report_1_params = {
        'ClOrdID': new_order_single_1_params['ClOrdID'],
        'OrderID': "*",
        'ExecID': "*",
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_single_1_params['OrderQty'],
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'Price': new_order_single_1_params['Price'],
        'OrderQty': new_order_single_1_params['OrderQty']
    }
    bca.verify_response(
        'Receive ExecutionReport1 ord1',
        bca.create_filter('ExecutionReport', execution_report_1_params),
        enter_order_1,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )

    execution_report_2_params = copy.deepcopy(execution_report_1_params)
    execution_report_2_params['OrdStatus'] = 0
    execution_report_2_params['ExecType'] = 0
    bca.verify_response(
        'Receive ExecutionReport2 ord1',
        bca.create_filter('ExecutionReport', execution_report_2_params),
        enter_order_1,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )

    new_order_single_2_params = {
        'ClOrdID': bca.client_orderid(9),
        # 'Parties': "",
        'Account': "KEPLER",
        'HandlInst': '2',
        'Instrument': case_params['Instrument'],
        'Side': case_params['Side_ord2'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': case_params['OrderQty_ord2'],
        'OrdType': '2',
        'Price': case_params['Price_ord2']
    }
    enter_order_2 = bca.act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder ord2',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_single_2_params)
        ))
# TODO! countinue refactor
    execution_report_2_params = {
        'ClOrdID': new_order_single_2_params['ClOrdID'],
        'OrderID': "*",
        'ExecID': "*",
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'OrdStatus': '2',
        'ExecType': 'F',
        'LeavesQty': new_order_single_2_params['OrderQty'],
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'Price': new_order_single_2_params['Price'],
        'OrderQty': new_order_single_2_params['OrderQty']
    }
    execution_report_1f_params = {
        'ClOrdID': new_order_single_1_params['ClOrdID'],
        'OrderID': "*",
        'ExecID': "*",
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_single_1_params['OrderQty'],
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'Price': new_order_single_1_params['Price'],
        'OrderQty': new_order_single_1_params['OrderQty']
    }

    # build messages
    #
    # new_order_single_1 = utils.create_message('NewOrderSingle', new_order_single_1_params)
    # new_order_single_2 = utils.create_message('NewOrderSingle', new_order_single_2_params)
    # execution_report_1 = utils.create_filter("ExecutionReport", execution_report_1_params)
    # execution_report_2 = utils.create_filter("ExecutionReport", execution_report_2_params)
    # execution_report_1f = utils.create_filter("ExecutionReport", execution_report_1f_params)
    new_order_single_1 = bca.message_to_grpc('NewOrderSingle', new_order_single_1_params)
    new_order_single_2 = bca.message_to_grpc('NewOrderSingle', new_order_single_2_params)
    execution_report_1 = bca.create_filter("ExecutionReport", execution_report_1_params)
    execution_report_2 = bca.create_filter("ExecutionReport", execution_report_2_params)
    execution_report_1f = bca.create_filter("ExecutionReport", execution_report_1f_params)


    # create new event for test case
    #

    report_id = bca.create_event_id()
    bca.create_event(
        'quod_test' + datetime.now().strftime('%Y%m%d-%H:%M:%S'),
        report_id,
        parent_event_id
    )

    # send NewSingleOrder for order 1
    #

    pmreq_ord1 = act_fix_pb2.PlaceMessageRequest(
        message=new_order_single_1,
        connection_id=connectivity,
        parent_event_id=report_id,
        description='Send NewOrderSingle 1'
    )
    with grpc.insecure_channel(ACT) as channel:
        pmresp_ord1_new = act_fix_pb2_grpc.ActStub(channel).placeOrderFIX(pmreq_ord1)

    #

    checkpoint = pmresp_ord1_new.checkpoint_id
    # print("Received {}".format(pmresp_ord1_new.response_message.metadata.message_type))

    crreq_ord1_new = verifier_pb2.CheckRuleRequest(
        connectivity_id=connectivity,
        filter=execution_report_1,
        checkpoint=checkpoint,
        timeout=3000,
        parent_event_id=report_id,
        description='Receive ExecutionReport for ord1 (OrderStatus = A)'
    )
    with grpc.insecure_channel(VERIFIER) as channel:
        answer1 = verifier_pb2_grpc.VerifierStub(channel).submitCheckRule(crreq_ord1_new)
    # print("Status: {}".format(answer1.status))

    pmreq_ord2 = act_fix_pb2.PlaceMessageRequest(
        message=new_order_single_2,
        connection_id=connectivity,
        parent_event_id=report_id,
        description='Send NewOrderSingle 2'
    )
    with grpc.insecure_channel(ACT) as channel:
        pmresp_ord2 = act_fix_pb2_grpc.ActStub(channel).placeOrderFIX(pmreq_ord2)
    # print("Act response 2 fields: {}".format(pmresp_ord2.response_message.fields))

    crreq_ord2_filled = verifier_pb2.CheckRuleRequest(
        connectivity_id=connectivity,
        filter=execution_report_2,
        checkpoint=checkpoint,
        timeout=3000,
        parent_event_id=report_id,
        description='Receive ExecutionReport 2'
    )
    with grpc.insecure_channel(VERIFIER) as channel:
        answer2 = verifier_pb2_grpc.VerifierStub(channel).submitCheckRule(crreq_ord2_filled)

    crreq_ord1_filled = verifier_pb2.CheckRuleRequest(
        connectivity_id=connectivity,
        filter=execution_report_1f,
        checkpoint=checkpoint,
        timeout=3000,
        parent_event_id=report_id,
        description='Receive ExecutionReport 2'
    )
    with grpc.insecure_channel(VERIFIER) as channel:
        answer3 = verifier_pb2_grpc.VerifierStub(channel).submitCheckRule(crreq_ord1_filled)